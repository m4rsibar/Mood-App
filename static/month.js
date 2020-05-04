var canvas = document.getElementById("canvas").getContext("2d");
var gradientStroke = canvas.createLinearGradient(0, 0, 1800, 0);
var monthInput = document.getElementById("month");
gradientStroke.addColorStop(0, "#F02FC2");
gradientStroke.addColorStop(0.5, "#6094EA");
gradientStroke.addColorStop(1, "#49d0eb");

// window.onload = () => {
//   var userMonth = getCookie("userMonth");
//   document.getElementById("select").innerHTML = userMonth;
// };

ChartInit();
let moodgraph;
async function ChartInit() {
  const data = await getData();
  moodgraph = new Chart(canvas, {
    type: "line",
    data: {
      datasets: [
        {
          label: "Mood",
          data: info.monthdata,
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
          borderWidth: 4,
          responsive: true,
        },
      ],
    },
    options: {
      tooltips: {
        callbacks: {
          label: function (tooltipItem, data) {
            var dataLabel = info.comments[tooltipItem.index];
            return dataLabel;
          },
        },
      },
      legend: {
        display: true,
      },
      responsive: false,
      scales: {
        yAxes: [
          {
            ticks: {
              display: true,
              beginAtZero: true,
              suggestedMax: 5,
            },
            scaleLabel: {
              display: true,
              labelString: "Mood Rating",
            },
          },
        ],
        xAxes: [
          {
            type: "linear",
            position: "bottom",
            ticks: {
              stepSize: 1,
              max: 31,
            },
            scaleLabel: {
              display: true,
              labelString: "Day of Month",
            },
            gridLines: {
              drawOnChartArea: false,
            },
            display: true,
          },
        ],
      },
    },
  });
}

async function getData() {
  let monthdata = [];
  let comments = [];
  let dates = [];
<<<<<<< HEAD
  let avaliableMonths = [];
  let avaliableYears = [];

  const res = await fetch("https://mood-visualization.herokuapp.com/month");
=======
  const res = await fetch("http://127.0.0.1:5000/month");
>>>>>>> parent of 6ef4816... added sample dataset
  const data = await res.json();
  for (var i = 0, l = data.result.length; i < l; i++) {
    monthdata[i] = {
      x: data.result[i].day,
      y: data.result[i].moodrating,
    };
    comments.push(data.result[i].comment);
    dates.push(data.result[i].date);
  }
  // for (var i = 0, l = data.avaliableDates.length; i < l; i++) {
  //   avaliableMonths.push(data.avaliableDates[i].month);
  //   avaliableYears.push(data.avaliableDates[i].year);
  // }

  return (info = {
    monthdata,
    comments,
    dates,
    // avaliableMonths,
    // avaliableYears,
  });
}

// async function PopulateDropdown() {
//   const avaliableDates = await getData();
//   var select = document.getElementById("select"),
//     arr = avaliableDates.avaliableMonths;

//   monthName = (mon) => {
//     return [
//       "January",
//       "February",
//       "March",
//       "April",
//       "May",
//       "June",
//       "July",
//       "August",
//       "September",
//       "November",
//       "December",
//     ][mon - 1];
//   };

//   for (var i = 0; i < arr.length; i++) {
//     var option = document.createElement("OPTION"),
//       txt = document.createTextNode(monthName(arr[i]));
//     option.appendChild(txt);
//     option.setAttribute("value", arr[i]);
//     select.insertBefore(option, select.lastChild);
//   }
// }

// PopulateDropdown();
