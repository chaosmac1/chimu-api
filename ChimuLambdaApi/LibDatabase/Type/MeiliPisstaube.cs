namespace ChimuLambdaApi; 

public class MeiliPisstaube {
    public long Id { get; set; }
    public int RankedStatus { get; set; }
    public string? Artist { get; set; } 
    public string? Title { get; set; }
    public string? Creator { get; set; }
    public List<string>? Tags { get; set; }
    public List<int>? Mode { get; set; }
    public List<string>? DiffName { get; set; }
    public List<float>? Cs { get; set; }
    public List<float>? Ar { get; set; }
    public List<float>? Od { get; set; }
    public List<float>? Hp { get; set; }
    public List<double>? DifficultyRating { get; set; }
    public List<double>? Bpm { get; set; }
    public List<int>? TotalLength { get; set; }
    public int Genre { get; set; }
    public int Language { get; set; }
    public DateTime ApprovedDate { get; set; }
}