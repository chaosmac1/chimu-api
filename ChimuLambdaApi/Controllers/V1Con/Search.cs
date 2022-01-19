using System.Net;
using System.Text;
using System.Web.Http;
using ChimuLambdaApi.LibDatabase;
using Index = Meilisearch.Index;

namespace ChimuLambdaApi.Controllers.V1Con;

public static class Search {
    public static V1Controller.GetSearchBeatmapSetRes SearchBy(ref LibDatabase.Search.FindBeatmapValue findBy) {
        IEnumerable<MeiliPisstaube> res;
        {
            Index? meilIndex = GetDb.GetDbBeatmap();
            if (meilIndex is null)
                return new V1Controller.GetSearchBeatmapSetRes() { code = 409, message = String.Empty };
            res = LibDatabase.Search.FindBeatmaps(meilIndex, ref findBy);
        }
        
        
        if (!res.Any())
            throw new HttpResponseException(HttpStatusCode.NotFound);

        var beatmapSetIdsBuilder = new StringBuilder();
        foreach (var beatmap in res)
            beatmapSetIdsBuilder.Append($"{beatmap.Id},");
        var beatmapSetIds = beatmapSetIdsBuilder.ToString();
        beatmapSetIds = beatmapSetIds[..^1];

        try {
            var mysql = GetDb.GetMysql();
            if (mysql is null)
                return new V1Controller.GetSearchBeatmapSetRes {
                    code = 409,
                    data = new List<V1Controller.BeatmapSetPlusChilds>(0),
                    message = "Conflict on the server"
                };
            var sql = mysql.CreateCommand();

            sql.CommandText = @$"SELECT * FROM BeatmapSet WHERE SetId IN ({beatmapSetIds})";
            var reader = sql.ExecuteReader();
            if (!reader.HasRows)
                return new V1Controller.GetSearchBeatmapSetRes {
                    code = 404,
                    data = new List<V1Controller.BeatmapSetPlusChilds>(0),
                    message = "Not Found"
                };

            var beatmapSetRaw = new Dictionary<int, V1Controller.BeatmapSetPlusChilds>(100);
            while (reader.Read())
                beatmapSetRaw.Add((int) reader[0], new V1Controller.BeatmapSetPlusChilds {
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
                    ChildrenBeatmaps = new List<V1Controller.BeatmapSetPlusChilds.BeatmapChild>(10)
                });


            reader.Close();
            sql = mysql.CreateCommand();
            sql.CommandText = @$"SELECT * FROM Beatmaps WHERE ParentSetId IN ({beatmapSetIds})";
            reader = sql.ExecuteReader();

            while (reader.Read()) {
                var set = beatmapSetRaw[(int) reader[1]];
                set.ChildrenBeatmaps ??= new List<V1Controller.BeatmapSetPlusChilds.BeatmapChild>(10);
                set.ChildrenBeatmaps.Add(new V1Controller.BeatmapSetPlusChilds.BeatmapChild {
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
                    DownloadPath = $"/d/{(int) reader[1]}"
                });
            }

            reader.Close();

            var data = new List<V1Controller.BeatmapSetPlusChilds>(beatmapSetRaw.Count);
            foreach (var i in beatmapSetRaw) data.Add(i.Value);


            return new V1Controller.GetSearchBeatmapSetRes {
                code = 0,
                data = data,
                message = string.Empty
            };
        }
#if DEBUG
        catch (Exception e) {
            Console.WriteLine(e);
            throw;
        }
#else
        catch (Exception) {
            return new HttpResponseMessage() {
                StatusCode = HttpStatusCode.Conflict,
            };
        }
#endif
    }
}