function makeRepoGraph(repoMetrics, rname) {
    var repoData = {
        labels : repoMetrics.labels,
        datasets : [
            { 
                fillColor : "rgba(160,30,50,0)",
                strokeColor : "rgba(160,30,50,0.5)",
                pointColor : "rgba(160,30,50,0.5)",
                pointStrokeColor : "#fff",
                data : repoMetrics.fork
            },
            { 
                fillColor : "rgba(70, 160, 210,0)",
                strokeColor : "rgba(70, 160, 210,0.5)",
                pointColor : "rgba(70, 160, 210,0.5)",
                pointStrokeColor : "#fff",
                data : repoMetrics.closed_issue
            },
            { 
                fillColor : "rgba(100, 100, 100,0)",
                strokeColor : "rgba(100, 100, 100,.5)",
                pointColor : "rgba(100, 100, 100,.5)",
                pointStrokeColor : "#fff",
                data : repoMetrics.star
            }
        ]
    };
    var canvas = $("#" + rname);
    canvas.attr({
        "height": "300",
        "width": "750"
    });
    var opts = {scaleShowGridLines: false};
    var ctx = canvas[0].getContext('2d');
    var myNewGraph = new Chart(ctx).Line(repoData, opts); 

}


function createCORSRequest(method, url){
    var xhr = new XMLHttpRequest();
    if ("withCredentials" in xhr){
        xhr.open(method, url, true);
    } else if (typeof XDomainRequest != "undefined"){
        xhr = new XDomainRequest();
        xhr.open(method, url);
    } else {
        xhr = null;
    }
    return xhr;
}


listCharts = function(chartContainer, indicatorList, graphData) {
    var repos = [];
    for (var key in graphData) {
        repos.push(key);
    }

    for (var i=0; i<repos.length; i++) {

        // Fill the carousel indicators
        var ind_attribs = {"data-target": "#chartCarousel",
            "data-slide-to": i+''};
        var target = $("<li></li>").attr(ind_attribs);

        // Fill in the carousel items, include a title and a canvas
        var canvas_attribs = {class: "repo chart", id: repos[i]};
        var chartItem = $("<div></div>").attr("class", "item");

        chartTitle = $("<div></div>").attr("class", "chart title");
        chartTitle.text(repos[i]);
        chartItem.append(chartTitle);
        chartItem.append($("<canvas></canvas>").attr(canvas_attribs));

        if (i==0) {
            target.attr("class", "active");
            chartItem.attr("class", "active item");
        }
        indicatorList.append(target);      
        chartContainer.append(chartItem);
    }
}


$(function(){

    var charturl = "https://s3.amazonaws.com/data.codeforamerica.org/repos/hist.json";
    var chartRequest = createCORSRequest("get", charturl);
    var chartResponse = {};
    if (chartRequest) {
        chartRequest.onload = function(){
            chartResponse = JSON.parse(chartRequest.responseText);
            listCharts($(".carousel-inner"), $(".carousel-indicators"), chartResponse);
            $(".repo.chart").each(function(i, el){ 
                var repoName = $(el).attr("id");
                makeRepoGraph(chartResponse[repoName], repoName);
            });
        }
        chartRequest.send();
    }


    var totalsUrl = "https://s3.amazonaws.com/data.codeforamerica.org/repos/totals.json";
    var totalsRequest = createCORSRequest("get", totalsUrl);
    var totalsResponse = {};
    if (totalsRequest) {
        totalsRequest.onload = function(){
            totalsResponse = JSON.parse(totalsRequest.responseText);
            $("#issues-total").text(totalsResponse.total_closed_issues);
            $("#forks-total").text(totalsResponse.total_forks);
        }
        totalsRequest.send();
    }

});