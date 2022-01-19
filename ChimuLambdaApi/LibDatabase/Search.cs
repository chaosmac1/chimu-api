using System.Text;
using Meilisearch;
using Index = Meilisearch.Index;

namespace ChimuLambdaApi.LibDatabase; 

public static class Search {
    public static IEnumerable<MeiliPisstaube> FindBeatmaps(Index meiliIndex, ref FindBeatmapValue props) {
        var filterBuilder = new StringBuilder(20);

        if (props.Mode != -1)
            filterBuilder.Append($"mode = {props.Mode} ");

        if (props.Status != -5) {
            if (props.Query != "" && filterBuilder.Length == 0)
                filterBuilder.Append(" AND ");

            filterBuilder.Append(props.Status switch {
                1 or 2 => "(rankedStatus = 1 OR rankedStatus = 2) ",
                _ => $"rankedStatus = {props.Status} "
            });
        }

        static void AndAppendIf0(StringBuilder builder, string? value) {
            if (string.IsNullOrEmpty(value)) return;
            if (builder.Length != 0)
                builder.Append("AND ");
            builder.Append(value);
        }

        // AR
        if (props.MinAr != -1)
            AndAppendIf0(filterBuilder, $"ar >= {props.MinAr} ");

        if (props.MaxAr != -1)
            AndAppendIf0(filterBuilder, $"ar <= {props.MaxAr} ");

        // OD
        if (props.MinOd != -1)
            AndAppendIf0(filterBuilder, $"od >= {props.MinOd} ");

        if (props.MaxOd != -1)
            AndAppendIf0(filterBuilder, $"od <= {props.MaxOd} ");

        // CS
        if (props.MinCs != -1)
            AndAppendIf0(filterBuilder, $"cs >= {props.MinCs} ");

        if (props.MaxCs != -1)
            AndAppendIf0(filterBuilder, $"cs <= {props.MaxCs} ");

        // HP
        if (props.MinHp != -1)
            AndAppendIf0(filterBuilder, $"hp >= {props.MinHp} ");

        if (props.MaxHp != -1)
            AndAppendIf0(filterBuilder, $"hp <= {props.MaxHp} ");

        // Diff
        if (props.MinDiff != -1)
            AndAppendIf0(filterBuilder, $"difficultyRating >= {props.MinDiff} ");

        if (props.MaxDiff != -1)
            AndAppendIf0(filterBuilder, $"difficultyRating <= {props.MaxDiff} ");

        // Bpm
        if (props.MinBpm != -1)
            AndAppendIf0(filterBuilder, $"bpm >= {props.MinBpm} ");

        if (props.MaxBpm != -1)
            AndAppendIf0(filterBuilder, $"bpm <= {props.MaxBpm} ");

        // Length
        if (props.MinLength != -1)
            AndAppendIf0(filterBuilder, $"totalLength >= {props.MinLength} ");

        if (props.MaxLength != -1)
            AndAppendIf0(filterBuilder, $"totalLength <= {props.MaxLength} ");

        // Genre
        if (props.Genre != -1)
            AndAppendIf0(filterBuilder, $"genre = {props.Genre} ");

        // Language
        if (props.Language != -1)
            AndAppendIf0(filterBuilder, $"language = {props.Language} ");


        try {
            var taskRes = meiliIndex.Search<MeiliPisstaube>(filterBuilder.ToString(), new SearchQuery {
                AttributesToHighlight = new[] {"title", "artist", "tags", "creator", "diffName"},
                Limit = props.Amount,
                Offset = props.Offset,
                Filter = filterBuilder.ToString(),
                Matches = true
            });
            if (taskRes is null) return new List<MeiliPisstaube>(0);
            taskRes.Wait();
            var res = taskRes.Result;
            if (res is null) return new List<MeiliPisstaube>(0);

            return res.Hits;
        }
#if DEBUG
        catch (Exception e) {
            Console.WriteLine(e);
            throw;
        }
#else
        catch (Exception) { return Array.Empty<Beatmap>(); }
#endif
    }

    public readonly record struct FindBeatmapValue(
        string Query,
        int Amount,
        int Offset,
        long Status,
        long Mode,
        long MinAr,
        long MaxAr,
        long MinOd,
        long MaxOd,
        long MinCs,
        long MaxCs,
        long MinHp,
        long MaxHp,
        long MinDiff,
        long MaxDiff,
        long MinBpm,
        long MaxBpm,
        long MinLength,
        long MaxLength,
        long Genre,
        long Language
    );
}