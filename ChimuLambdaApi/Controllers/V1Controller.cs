using System.Net;
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

    /// <summary> In Python get_map.get_map </summary>
    /// <param name="id"> map_id </param>
    [HttpGet("map")]
    public GetSearchBeatmapSetRes GetBeatmap(long id) {
        var sql = GetDb.GetMysql()?.CreateCommand();
        if (sql is null)
            return new GetSearchBeatmapSetRes() { code = 409, message = String.Empty };
        sql.CommandText = $"SELECT * FROM Beatmaps WHERE BeatmapId = {id} LIMIT 1";
        var reader = sql.ExecuteReader();
        reader.Read();
        if (!reader.HasRows) return new GetSearchBeatmapSetRes() {
            code = 404,
            message = "Not Found",
        };

        return new GetSearchBeatmapSetRes() {
            code = 0,
            message = string.Empty,
            data = new BeatmapSetPlusChilds.BeatmapChild() {
                BeatmapId = (int) reader[0],
                ParentSetId = (int) reader[1],
                DiffName = (string) reader[2],
                FileMD5 = (string) reader[3],
                Mode = (int) reader[4],
                BPM = (double) reader[5],
                AR = (float) reader[6],
                OD = (float) reader[7],
                CS = (float) reader[8],
                HP = (float) reader[9],
                TotalLength = (int) reader[10],
                HitLength = (long) reader[11],
                Playcount = (int) reader[12],
                Passcount = (int) reader[13],
                MaxCombo = (long) reader[14],
                DifficultyRating = (double) reader[15],
                OsuFile = (string) reader[16],
                DownloadPath = $"/d/{reader[1]}",
            }
        };
    }

    [HttpGet("set/{id}")]
    public GetSearchBeatmapSetRes GetBeatmapJson(long id) {
         var sql = GetDb.GetMysql()?.CreateCommand();
         if (sql is null) return new GetSearchBeatmapSetRes() {code = 409, message = ""};
         sql.CommandText = $"SELECT * FROM BeatmapSet WHERE SetId = {id} LIMIT 1;";
        var reader = sql.ExecuteReader();
        reader.Read();
        if (!reader.HasRows) 
            return new GetSearchBeatmapSetRes() {
                code = 404,
                message = "Not Found"
            };

        BeatmapSetPlusChilds res = new() {
            SetId = (int) reader[0],
            RankedStatus = (int) reader[1],
            ApprovedDate = (DateTime) reader[2],
            LastUpdate = (DateTime) reader[3],
            LastChecked = (DateTime) reader[4],
            Artist = (string) reader[5],
            Title = (string) reader[6],
            Creator = (string) reader[7],
            Source = (string) reader[8],
            Tags = (string) reader[9],
            HasVideo = (bool) reader[10],
            Genre = (int) reader[11],
            Language = (int) reader[12],
            Favourites = (long) reader[13],
            Disabled = (bool) reader[14],
            IpfsHash = (string) reader[15],
            ChildrenBeatmaps = new List<BeatmapSetPlusChilds.BeatmapChild>(10)
        };
        reader.Close();

        sql = GetDb.GetMysql()?.CreateCommand();
        if (sql is null) return new GetSearchBeatmapSetRes() {code = 409, message = "" };
        
        sql.CommandText = $"SELECT * FROM Beatmaps WHERE ParentSetId = {id}";
        reader = sql.ExecuteReader();
        while (reader.Read()) {
            res.ChildrenBeatmaps.Add(new V1Controller.BeatmapSetPlusChilds.BeatmapChild {
                BeatmapId = (int) reader[0],
                ParentSetId = (int) reader[1],
                DiffName = (string) reader[2],
                FileMD5 = (string) reader[3],
                Mode = (int) reader[4],
                BPM = (double) reader[5],
                AR = (float) reader[6],
                OD = (float) reader[7],
                CS = (float) reader[8],
                HP = (float) reader[9],
                TotalLength = (int) reader[10],
                HitLength = (long) reader[11],
                Playcount = (int) reader[12],
                Passcount = (int) reader[13],
                MaxCombo = (long) reader[14],
                DifficultyRating = (double) reader[15],
                OsuFile = (string) reader[16],
                DownloadPath = $"/d/{(int) reader[1]}",
            });
        }

        return new GetSearchBeatmapSetRes() {
            code = 0,
            message = string.Empty,
            data = new List<BeatmapSetPlusChilds>()
        };
    }

    
    
    [HttpGet("download/{id}")]
    public ActionResult GetDownload(long id, short? n) {
        bool noVideo = n is 1;

        var beatmap = LibDatabase.RedistRequest.RequestDownload(id, noVideo)?.ToDictionary();
        if (beatmap is null || beatmap.Count == 0) return new NotFoundResult();
        
        return Redirect($"https://ipfs.chimu.moe/ipfs/{beatmap["IpfsHash"]}?filename={System.Web.HttpUtility.UrlEncode((string) beatmap["File"])}");
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
        public List<BeatmapChild>? ChildrenBeatmaps { get; set; }

        public class BeatmapChild {
            public int BeatmapId { get; set; }
            public int ParentSetId { get; set; }
            public string? DiffName { get; set; }
            public string? FileMD5 { get; set; }
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
            public string? OsuFile { get; set; }
            public string? DownloadPath { get; set; }
        }
    }

    public class GetSearchBeatmapSetRes {
        public int code { get; set; }
        public string? message { get; set; }
        public object? data { get; set; }
    }
}