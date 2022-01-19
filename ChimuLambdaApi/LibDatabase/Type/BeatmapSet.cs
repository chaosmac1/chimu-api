namespace ChimuLambdaApi;

/// <summary> In Db </summary>
public class BeatmapSet {
    public int SetId { get; set; }
    public int RankedStatus { get; set; }
    public DateTime ApprovedDate { get; set; }
    public DateTime LastUpdate { get; set; }
    public DateTime LastChecked { get; set; }
    public string Artist { get; set; }
    public string Title { get; set; }
    public string Creator { get; set; }
    public string Source { get; set; }
    public string Tags { get; set; }
    public bool HasVideo { get; set; }
    public int Genre { get; set; }
    public int Language { get; set; }
    public long Favourites { get; set; }
    public bool Disabled { get; set; }
    public string IpfsHash { get; set; }
}