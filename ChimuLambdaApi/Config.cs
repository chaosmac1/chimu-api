namespace ChimuLambdaApi;

public static class Config {
    public static class MeiliSearch {
        private const string _address = "";
        private const string _masterKey = "";
        private const string _index = "";

        public static string Address =>
            _address.Length > 0 ? _address : throw new Exception(nameof(_address) + " is \"\"");

        public static string MasterKey =>
            _masterKey.Length > 0 ? _masterKey : throw new Exception(nameof(_masterKey) + " is \"\"");

        public static string Index => _index.Length > 0 ? _index : throw new Exception(nameof(_index) + " is \"\"");
    }

    public static class Files {
        private const string _beatmapDir = "";

        public static string BeatmapDir =>
            _beatmapDir != "" ? _beatmapDir : throw new Exception(nameof(_beatmapDir) + " is \"\"");
    }

    public static class MySql {
        private const string _passwd = "";
        private const string _username = "";
        private const int _port = 0;
        private const string _url = "";
        private const string _db = "";
        public static string Passwd => _passwd != "" ? _passwd : throw new Exception(nameof(_passwd) + " is \"\"");

        public static string Username =>
            _username != "" ? _username : throw new Exception(nameof(_username) + " is \"\"");

        public static int Port => _port != 0 ? _port : throw new Exception(nameof(_port) + " is  0");
        public static string Url => _url != "" ? _url : throw new Exception(nameof(_url) + " is \"\"");
        public static string Db => _db != "" ? _db : throw new Exception(nameof(_db) + " is \"\"");
    }
    
    public static class Redis {
        private const string _address = "";
        private const string _db = "";
        private const int _port = 0;
        private const string _passwd = "";
        public static string Address => _address.Length != 0? _address: throw new Exception(nameof(_address) + " is \"\"");
        public static string Db => _db.Length != 0? _db: throw new Exception(nameof(_db) + " is \"\"");
        public static int Port => _port != 0 ? _port : throw new Exception(nameof(_port) + " is  0");
        public static string Passwd => _passwd != "" ? _passwd : throw new Exception(nameof(_passwd) + " is \"\"");
    }
}