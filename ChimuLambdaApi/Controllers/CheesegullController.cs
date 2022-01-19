// using System.Net;
// using Microsoft.AspNetCore.Mvc;
// using System.Diagnostics;
// using System.Net;
// using System.Net.Http;
// using System.Threading.Tasks;
// using System.Web;
//
// namespace ChimuLambdaApi.Controllers;
//
// [ApiController]
// [Route("/")]
// public class CheesegullController : ControllerBase {
//     private readonly ILogger<CheesegullController> _logger;
//
//     public CheesegullController(ILogger<CheesegullController> logger) => _logger = logger;
//
//     [HttpGet(Name = "/cheesegull/b")]
//     public Task<HttpResponseMessage> GetBeatmap(long id) {
//         throw new NotImplementedException(nameof(GetBeatmap));
//     }
//
//     [HttpGet(Name = "/cheesegull/md5")]
//     public Task<HttpResponseMessage> GetBeatmapByMd5(string md5) {
//         throw new NotImplementedException(nameof(GetBeatmapByMd5));
//     }
//
//     [HttpGet(Name = "/cheesegull/s")]
//     public Task<HttpResponseMessage> GetBeatmapSet(long id)
//         => throw new NotImplementedException(nameof(GetBeatmapSet));
//
//     [HttpGet(Name = "/cheesegull/search")]
//     public Task<HttpResponseMessage> GetSearchBeatmapSet(
//         string query = "",
//         long disco = 1,
//         long amount = 1,
//         long offset = 0,
//         long status = 0,
//         long mode = 0
//     ) {
//         throw new NotImplementedException(nameof(GetSearchBeatmapSet));
//     }
// }

