#nullable enable
using Meilisearch;
using Npgsql;
using StackExchange.Redis;
using Index = Meilisearch.Index;

namespace ChimuLambdaApi.LibDatabase;

public static class GetDb {
    public static Index? GetDbBeatmap() {
        var client = new MeilisearchClient(Config.MeiliSearch.Address, Config.MeiliSearch.MasterKey);
        client.Health().Wait();
        var index = client.Index(Config.MeiliSearch.Index);

        var synonyms = new Dictionary<string, IEnumerable<string>>();
        synonyms.Add("rankingRules", new List<string> {
            "desc(approvedDate)",
            "typo",
            "words",
            "proximity",
            "attribute",
            "wordsPosition",
            "exactness"
        });

        index.UpdateSettings(new Settings {
            Synonyms = synonyms
        });

        return index;
    }

    public static NpgsqlConnection? GetMysql() {
        var connStringBuilder = new NpgsqlConnectionStringBuilder();
        connStringBuilder.Host = Config.MySql.Url;
        connStringBuilder.Port = Config.MySql.Port;
        connStringBuilder.Password = Config.MySql.Passwd;
        connStringBuilder.Username = Config.MySql.Username;
        connStringBuilder.Database = Config.MySql.Db;
        var conn = new NpgsqlConnection(connStringBuilder.ConnectionString);
        try {
            conn.Open();
            return conn;
        }
#if DEBUG
        catch (Exception e) {
            Console.WriteLine(e);
            throw;
        }
#else
        catch (Exception) { return null; }
#endif
    }
    
    public static ConnectionMultiplexer? GetRedis() => LazyConnection?.Value;
    
    public static IDatabase? GetRedisDataBase() => GetRedis()?.GetDatabase();


    private static Lazy<ConnectionMultiplexer> LazyConnection = LazyConnectionInit();
    
    private static Lazy<ConnectionMultiplexer> LazyConnectionInit() {
        Console.WriteLine("Redis: Initializing...");
        try {
            LazyConnection = new Lazy<ConnectionMultiplexer>(() => {
                var configurationOptions = new ConfigurationOptions() {
                    Password = Config.Redis.Passwd,
                };
                configurationOptions.EndPoints.Add(host: Config.Redis.Address, port: Config.Redis.Port);
                return ConnectionMultiplexer.Connect(configurationOptions);
            });

            Console.WriteLine("Ping Test");
            if (!LazyConnection.Value.GetDatabase().PingAsync().Wait(1000)) {
                Console.WriteLine("Redis: Couldn\'t establish a redis connection!");
                Console.WriteLine("Exiting...");
                System.Environment.Exit(1);
            }
            Console.WriteLine("Redis: Succeded.");
            Console.WriteLine("Redis: Setup redis pub/sub");
            
            Console.WriteLine("Redis: Subscribe Not Implemented ");
            
            
            var subscriber = LazyConnection.Value.GetSubscriber();
            
            subscriber.Subscribe(new RedisChannel("chimu:s:downloads", RedisChannel.PatternMode.Auto),
                RedistRequest.SubscribeDownloadResponseHandler);
            
            return LazyConnection;
        }
#if DEBUG
        catch (Exception e) {
            Console.WriteLine(e);
            throw;
        }
#else
        catch(Exception) { return null; }
#endif    
    }
}