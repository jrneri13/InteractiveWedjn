
// Selector list to append options to
var selectDiv = document.getElementById("selDataset");

// Add options to list
Plotly.d3.json("/names", function (error, response) {
    if (error) return console.warn(error);
    var IDs = response;
    for (var i = 0; i < IDs.length; i++) {
        var option = document.createElement("option");
        option.value = IDs[i];
        option.text = IDs[i];
        selectDiv.appendChild(option);
    }
})


// Pie chart
Plotly.d3.json("/samples/BB_940", function (error, response) {
    if (error) return console.warn(error);
    var data = [{
        values: response.sample_values.slice(0, 10),
        labels: response.otu_ids.slice(0, 10),
        type: 'pie'
    }];
    var layout = {
        autosize: false,
        width: 450,
        height: 430,
        margin: {
            l: 50,
            r: 50,
            b: 50,
            t: 50
        }
    };
    Plotly.plot("pie", data, layout);
})

// Bubble chart
Plotly.d3.json("/samples/BB_940", function (error, response) {
    if (error) return console.warn(error);
    var data = [{
        x: response.otu_ids,
        y: response.sample_values,
        mode: 'markers',
        marker: {
            color: response.otu_ids,
            size: response.sample_values
        }
    }];
    var layout = {
        height: 600,
        width: 900,
        title: "Belly Button Bubble Chart",
        xaxis: {
            title: "OTU IDs"
        },
        yaxis: {
            title: "Sample values"
        }
    };
    Plotly.plot("bubble", data, layout);
})

