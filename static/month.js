var canvas = document.getElementById("canvas").getContext("2d");
var gradientStroke = canvas.createLinearGradient(0, 0, 1800, 0);
gradientStroke.addColorStop(0, "#F02FC2");
gradientStroke.addColorStop(0.5, "#6094EA");
gradientStroke.addColorStop(1, "#49d0eb");

ChartInit();

async function ChartInit() {
  const data = await getData();
  var moodgraph = new Chart(canvas, {
    type: "line",
    data: {
      labels: [1, 2, 3, 4],
      datasets: [
        {
          label: "Mood",
          data: data,
          backgroundColor: gradientStroke,
          borderColor: gradientStroke,
          pointBorderColor: gradientStroke,
          pointBackgroundColor: gradientStroke,
          pointHoverBackgroundColor: gradientStroke,
          pointHoverBorderColor: gradientStroke,
          pointBorderWidth: 8,
          pointHoverRadius: 8,
          pointHoverBorderWidth: 1,
          pointRadius: 3,
          fill: false,
          borderWidth: 4
        }
      ]
    },
    options: {
      legend: {
        display: true
      },
      responsive: false,
      scales: {
        yAxes: [
          {
            ticks: {
              display: true,
              beginAtZero: true
            },
            display: true
          }
        ],
        xAxes: [
          {
            type: "linear",
            position: "bottom",
            ticks: {
              stepSize: 1,
              max: 31
            },
            gridLines: {
              drawOnChartArea: false
            },
            display: true
          }
        ]
      }
    }
  });
}

async function getData() {
  let monthdata = [];
  const res = await fetch("https://mood-visualization.herokuapp.com/month");
  const data = await res.json();
  for (var i = 0, l = data.result.length; i < l; i++) {
    monthdata[i] = {
      x: data.result[i].day,
      y: data.result[i].moodrating
    };
  }
  return monthdata;
}
