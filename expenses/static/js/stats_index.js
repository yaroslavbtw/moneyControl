let ctx = document.getElementById('myChart');
let monthCumulative = document.getElementById("cmchart");
const showChart=(data)=>{
    const [values,labels] = [Object.values(data.category_data).map(item=>item.amount),Object.keys(data.category_data)]
    ctx.style.height = '400px';
    ctx.style.width = '200px';
    new Chart(ctx, {
        type: 'doughnut',
        data: {
          labels: labels,
          datasets: [
            {
              label: "Expense Categories",
              backgroundColor:   [
                    'rgb(80,151,215)',
                    '#18bc9c',
                    'rgb(231,109, 132)',
                    'rgba(153, 102, 255, 1)',
                     '#18bc9c'
                ],
              data: values
            }
          ]
        },
        options: {
          maintainAspectRatio: false,
          plugins: {
              title: {
                display: true,
                text: 'Distribution per category (Last 3 months)'
              }
        }
    }});
}

const getCategoryData=()=>{
    if(ctx.classList.contains('chart_expenses_index'))
        url = "/expenses/three_months_summary/";
    else url = "/incomes/three_months_summary/";
    fetch(url).then(res=>res.json()).
    then(data=>
    {
      showChart(data);
    })
}


const getCumulativeIncome=()=>{
    if(monthCumulative.classList.contains('chart_expenses_index'))
        url = '/expenses/last_3months_expense_source_stats/';
    else url = "/incomes/last_3months_income_source_stats/";
    fetch(url).then(res=>res.json()).
    then(data=>
    {
      showCMChart(data);
    })
}


window.addEventListener('load',getCategoryData)

window.addEventListener('load',getCumulativeIncome)

const showCMChart=(data)=>{

let labels = []
const monthsdata = []
let keys = null;

for(let i=0;i<data.cumulative_income_data.length;i++){
  const element = data.cumulative_income_data[i]
  labels.push(Object.keys(element)[0])
  const vals = Object.values(element)[0]
  keys = Object.keys(vals)
  monthsdata.push(Object.values(vals))
}

const getMonthRep=(dateObj)=>{
  const strDate = new Date(dateObj).toDateString()
  const splitted = strDate.split(' ')
  return [splitted[1]+" "+splitted[3]]
}


let dataFirst = {
    label: getMonthRep(labels[0]),
    data: monthsdata[0],
    lineTension: 0,
    fill: false,
    borderColor: 'rgb(80,151,215)'
  };

let dataSecond = {
    label: getMonthRep(labels[1]),
    data: monthsdata[1],
    lineTension: 0,
    fill: false,
  borderColor:  'rgb(231,109, 132)',
  };

let thirdSecond = {
    label: getMonthRep(labels[2]),
    data: monthsdata[2],
    lineTension: 0,
    fill: false,
  borderColor:  '#18bc9c ',
  };
let monthsData = {
  labels: keys,
  datasets: [dataFirst, dataSecond,thirdSecond]
};

let chartOptions = {
    maintainAspectRatio: false,
    plugins: {
      title: {
        display: true,
        text: 'Category Cumulative Comparison (Last 3 months)'
      }}
    ,
  legend: {
    display: true,
    position: 'top',
    labels: {
      boxWidth: 10,
    }
  }
};

monthCumulative.style.height = '400px';
monthCumulative.style.width = '200px';
new Chart(monthCumulative, {
  type: 'line',
  data: monthsData,
  options: chartOptions
});
}