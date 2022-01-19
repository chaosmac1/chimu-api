namespace ChimuLambdaApi;

/// <summary> In Db </summary>
public class Beatmap {
    public int BeatmapId { get; set; }
    public int ParentSetId { get; set; }
    public string DiffName { get; set; }
    public string FileMd5 { get; set; }
    public int Mode { get; set; }
    public double Bpm { get; set; }
    public float Ar { get; set; }
    public float Od { get; set; }
    public float Cs { get; set; }
    public float Hp { get; set; }
    public int TotalLength { get; set; }
    public long HitLength { get; set; }
    public int Playcount { get; set; }
    public int Passcount { get; set; }
    public long MaxCombo { get; set; }
    public double DifficultyRating { get; set; }
    public string File { get; set; }
}