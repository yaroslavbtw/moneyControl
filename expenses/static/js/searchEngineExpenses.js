const textAfterTable = $('#ShowingPages')
const textShowingPages = textAfterTable.text()
const objects = document.querySelectorAll('li.page-item')
arrayNav = []

objects.forEach((element)=>{
    if(element.classList.contains('disabled'))
        arrayNav.push(true)
    else arrayNav.push(false)
})

$(function (){
    $('#searchField').keyup(function (){
       $.ajax({
           type: "POST",
           url: "/expenses/search-expenses/",
           data: {
               'search_text': $('#searchField').val(),
               'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
           },
           success: searchSuccess,
           dataType: 'html'
       });
    });
});

function searchSuccess(data, textStatus, jqXHR)
{
    $('#expensesTable').html(data)
    if($('#searchField').val().length > 0)
    {
        textAfterTable.text('All results')
        const li_objects = document.querySelectorAll('li.page-item')
        li_objects.forEach((item)=>{
            if(!item.classList.contains('disabled'))
                item.classList.add('disabled')
        })
    }
    else
    {
        textAfterTable.text(textShowingPages)
        const li_objects = document.querySelectorAll('li.page-item')
        li_objects.forEach((item, num)=>{
            if(item.classList.contains('disabled') && !arrayNav[num])
                item.classList.remove('disabled')
        })
    }
    if(document.querySelectorAll('tr.element').length)
    {

    }
}