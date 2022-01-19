using System.ComponentModel;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using Newtonsoft.Json.Serialization;
using StackExchange.Redis;
namespace ChimuLambdaApi.LibDatabase; 

public static class RedistRequest {
    private static Dictionary<string, object> DownloadMap = new Dictionary<string, dynamic>(10000);
    private static string JsonConv(object value) {
        return JsonConvert.SerializeObject(value, Formatting.Indented, new JsonSerializerSettings() {
            ContractResolver = new DefaultContractResolver()
        });
    }
    
    public static RedisResult? Request(string key, Dictionary<string, object> obj) {
        var id = Guid.NewGuid().ToString();
        
        var redisDataBase = GetDb.GetRedisDataBase();
        if (redisDataBase is null) return null;

        obj["_ID"] = id;
        var inputData = JsonConv(obj);

        redisDataBase.Publish(
            new RedisChannel($"chimu:{key}", RedisChannel.PatternMode.Auto), new RedisValue(inputData));
        
        for (var i = 0; i < 15; i++) {
            if (!DownloadMap.TryGetValue(id, out var find)) {
                Task.Delay(new TimeSpan(TimeSpan.TicksPerMillisecond * 100));
                continue;
            }

            DownloadMap.Remove(id);
            return (dynamic)find;
        }
        
        return null;
    }

    public static RedisResult? RequestDownload(long id, bool noVideo)
        => Request("downloads", new Dictionary<string, object>() {
            {"SetId", id},
            {"NoVideo", noVideo}
        });
    
    /// <summary> Subscribe chimu:s:downloads </summary>
    /// <param name="channel"></param>
    /// <param name="value"></param>
    public static void SubscribeDownloadResponseHandler(RedisChannel channel, RedisValue value) {
        if (value.IsNullOrEmpty || !value.HasValue) return;
        dynamic json = JArray.Parse(value.ToString());
        
        DownloadMap[(string)json["_ID"]] = json;

    }
}





















