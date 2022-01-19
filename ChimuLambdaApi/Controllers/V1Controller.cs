using ChimuLambdaApi.LibDatabase;
using Microsoft.AspNetCore.Mvc;

namespace ChimuLambdaApi.Controllers;

[ApiController]
[Route("[controller]")]
public class V1Controller : ControllerBase {
    private readonly ILogger<V1Controller> _logger;

    public V1Controller(ILogger<V1Controller> logger) {
        _logger = logger;
    }

    // public static string JsonConv(object value) {
    //     return JsonConvert.SerializeObject(value, Formatting.Indented, new JsonSerializerSettings() {
    //         ContractResolver = new DefaultContractResolver()
    //     });
    // }

    [HttpGet("map")]
    public async Task<HttpResponseMessage> GetBeatmap(long id) {
        throw new NotImplementedException(nameof(GetBeatmap));
        HttpResponseMessage response;
        // Beatmap

        return response;
    }

    [HttpGet("set")]
    public Task<HttpResponseMessage> GetBeatmapJson(long id) {
        // BeatmapSet
        throw new NotImplementedException(nameof(GetBeatmapJson));
    }

    [HttpGet("download")]
    public ActionResult GetDownload(long id, short n) {
        throw new NotImplementedException($"{nameof(GetDownload)} Find File And Redirect to the URL");
        //return Redirect(URL);
    }

    [HttpGet("search")]
    public GetSearchBeatmapSetRes GetSearchBeatmapSet(
        string query = "",
        int amount = 100,
        int offset = 0,
        long status = -5,
        long mode = -1,
        long min_ar = -1,
        long max_ar = -1,
        long min_od = -1,
        long max_od = -1,
        long min_cs = -1,
        long max_cs = -1,
        long min_hp = -1,
        long max_hp = -1,
        long min_diff = -1,
        long max_diff = -1,
        long min_bpm = -1,
        long max_bpm = -1,
        long min_length = -1,
        long max_length = -1,
        long genre = -1,
        long language = -1
    ) {
        var findBy = new Search.FindBeatmapValue {
            Query = query,
            Amount = amount > 100 ? 100 : amount,
            Offset = offset,
            Status = status,
            Mode = mode,
            MinAr = min_ar,
            MaxAr = max_ar,
            MinOd = min_od,
            MaxOd = max_od,
            MinCs = min_cs,
            MaxCs = max_cs,
            MinHp = min_hp,
            MaxHp = max_hp,
            MinDiff = min_diff,
            MaxDiff = max_diff,
            MinBpm = min_bpm,
            MaxBpm = max_bpm,
            MinLength = min_length,
            MaxLength = max_length,
            Genre = genre,
            Language = language
        };

        return V1Con.Search.SearchBy(ref findBy);
    }

    public class BeatmapSetPlusChilds : BeatmapSet {
        public List<BeatmapChild> ChildrenBeatmaps { get; set; }

        public class BeatmapChild {
            public int BeatmapId { get; set; }
            public int ParentSetId { get; set; }
            public string DiffName { get; set; }
            public string FileMD5 { get; set; }
            public int Mode { get; set; }
            public double BPM { get; set; }
            public float AR { get; set; }
            public float OD { get; set; }
            public float CS { get; set; }
            public float HP { get; set; }
            public int TotalLength { get; set; }
            public long HitLength { get; set; }
            public int Playcount { get; set; }
            public int Passcount { get; set; }
            public long MaxCombo { get; set; }
            public double DifficultyRating { get; set; }
            public string OsuFile { get; set; }
            public string DownloadPath { get; set; }
        }
    }

    public class GetSearchBeatmapSetRes {
        public int code { get; set; }
        public string message { get; set; }
        public List<BeatmapSetPlusChilds> data { get; set; }
    }
}