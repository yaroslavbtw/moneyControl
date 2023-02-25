const ctx = document.getElementById('myChart');
const chr = document.getElementById('myChart2');

const renderChart = (data_chart) =>{
        const name = data_chart.nameChart
        const category_data = data_chart.category_data;
        const [labels, data] = [Object.keys(category_data), Object.values(category_data)];
        ctx.style.height = '300px';
        ctx.style.width = '200px';

        new Chart(ctx, {
        type: 'doughnut',
        data: {
          labels: labels,
          datasets: [{
            label: `Last 6 month ${name}`,
            data: data,
            borderWidth: 1
          }]
        },
        options: {
            maintainAspectRatio: false,
            title: {
                display: true,
                text: `${name} per category`,
            },
        }
        });
}

const getChartData=()=>{
    let url = '';
    if(ctx.classList.contains('chart_expense'))
        url = "/expenses/expenses_category_summary/";
    else url = "/incomes/incomes_source_summary/";
    $.ajax({
           type: "GET",
           url: url,
           success: (data_chart)=>{
               renderChart(data_chart);
               renderChart2(data_chart);
           } ,
           dataType: 'json',
       });
};

window.onload =  getChartData;


const renderChart2 = (data_chart)=> {
    const name = data_chart.nameChart
    const category_data = data_chart.category_data;
    const [labels, data] = [Object.keys(category_data), Object.values(category_data)];
    chr.style.height = '300px';
    chr.style.width = '200px';
    new Chart(chr, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: `Last 6 month ${name}`,
                data: data,
                borderWidth: 1,
                backgroundColor: "#18BC9C",
                borderColor: "#18BC9C",
            }]
        },
        options: {
            maintainAspectRatio: false,
            title: {
                display: true,
                text: `${name} per category`,
            },
        }
    });
}
