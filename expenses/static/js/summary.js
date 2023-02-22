const ctx = document.getElementById('myChart');

const renderChart = (data_expense) =>{
        const category_data = data_expense.expense_category_data;
        const [labels, data] = [Object.keys(category_data), Object.values(category_data)];
        ctx.style.height = '400px';
        ctx.style.width = '400px';

        new Chart(ctx, {
        type: 'doughnut',
        data: {
          labels: labels,
          datasets: [{
            label: 'Last 6 month expenses',
            data: data,
            borderWidth: 1
          }]
        },
        options: {
            maintainAspectRatio: false,
            title: {
                display: true,
                text: "Expenses per category",
            },
        }
        });
}

const getChartData=()=>{
    $.ajax({
           type: "GET",
           url: "/expenses/expenses_category_summary/",
           success: renderChart,
           dataType: 'json',
       });
};

getChartData();

