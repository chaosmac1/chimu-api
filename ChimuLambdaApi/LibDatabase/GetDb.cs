using Meilisearch;
using Npgsql;
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
}