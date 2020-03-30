let chart = document.getElementById("chart").getContext("2d");
var gradient = chart.createLinearGradient(0, 0, 2800, 0);
gradient.addColorStop(0, "rgba(232, 126, 240, .5)");
gradient.addColorStop(0.5, "rgba(126, 134, 240, .5)");
gradient.addColorStop(0.8, "rgb(161,214,227)");
gradient.addColorStop(0.1, "rgba(55, 201, 247,.5)");

ChartInit();

async function ChartInit() {
  const data = await getData();
  let moodgraph = new Chart(chart, {
    type: "bar",
    data: {
      labels: [
        "Sunday",
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday"
      ],
      comments: data.comments,
      datasets: [
        {
          label: "MoodRating",
          data: data.moods,
          backgroundColor: gradient
        }
      ]
    },
    options: {
      tooltips: {
        callbacks: {
          label: function(tooltipItem, data) {
            var dataLabel = data.comments[tooltipItem.index];
            return dataLabel;
          }
        }
      },
      responsive: true,
      scales: {
        yAxes: [
          {
            ticks: {
              suggestedMin: 0,
              suggestedMax: 5
            }
          }
        ]
      }
    }
  });
}

async function getData() {
  const moods = [];
  const dates = [];
  const comments = [];

  const res = await fetch("https://mood-visualization.herokuapp.com/thisweek");
  const data = await res.json();
  // console.log(data);
  data.result.forEach(i => {
    moods.push(i.moodrating), dates.push(i.date), comments.push(i.comment);
  });
  let object = { moods, dates, comments };
  return object;
}
