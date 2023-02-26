const ctx = document.getElementById('myChart');
const chr = document.getElementById('myChart2');

const renderChart = (data_json) =>{
    const data_chrt = data_json.data_chart
    const name = data_chrt.nameChart
    const values = Object.values(data_chrt.all_data.months)
    const letteredLabels = [
        "Jan",
        "Feb",
        "Mar",
        "Apr",
        "May",
        "Jun",
        "Jul",
        "Aug",
        "Sept",
        "Oct",
        "Nov",
        "Dec",
    ];
    ctx.style.height = '500px';
    ctx.style.width = '200px';

    new Chart(ctx, {
    type: 'line',
    data: {
      labels: letteredLabels,
      datasets: [{
        label: `This year ${name}`,
        data: values,
        borderWidth: 1
      }]
    },
    options: {
        maintainAspectRatio: false,
        plugins: {
        title: {
            display: true,
            text: `Year ${name}`,
        },
    }
    }});
}

const getChartData=()=>{
    let url = '';
    if(ctx.classList.contains('chart_expenses'))
        url = "/expenses/expenses-summary-rest/";
    else url = "/incomes/incomes-summary-rest/";
    $.ajax({
           type: "GET",
           url: url,
           success: (data_json)=>{
               console.log(data_json)
               renderChart(data_json);
               renderChart2(data_json);
           } ,
           dataType: 'json',
       });
};

window.onload =  getChartData;


const renderChart2 = (data_json)=> {
    const data_chrt = data_json.data_chart
    const name = data_chrt.nameChart
    const values = Object.values(data_chrt.all_data.days)
    const labels = ["Mon", "Tue", "Wed", "Thur", "Fri", "Sat", "Sun"];
    chr.style.height = '500px';
    chr.style.width = '200px';
    new Chart(chr, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: `This week ${name}`,
                data: values,
                borderWidth: 1,
                backgroundColor: "#18BC9C",
                borderColor: "#18BC9C",
            }]
        },
        options: {
            maintainAspectRatio: false,
            plugins: {
            title: {
                display: true,
                text: `Week ${name}`,
            },
        }
    }});
}