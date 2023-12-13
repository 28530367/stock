$.ajaxSetup({
    headers: { 'X-CSRFToken': csrf_token },
    type: 'POST',
});

function all_output(response) {
    $('#output').empty();

    for (var i = 0; i < response.length; i++) {
        var ticker_symbols = response[i]['ticker_symbols']
        var start_text = response[i]['start_text']
        var enddate_text = response[i]['enddate_text']
        var end_text = response[i]['end_text']

        var card = $('<div>').addClass('card mt-3 content');
        var ticker_header = $('<div>').addClass('card-header fs-5 fw-bold').text(ticker_symbols);
        var body = $('<div>').addClass('card-body');
        var start_header = $('<div>').addClass('card-header fs-5').text(start_text);
        var end_header = $('<div>').addClass('card-header fs-5').html(enddate_text + '<br>' + end_text);
        // 使用 CSS 將文字置中
        start_header.css('text-align', 'center');
        end_header.css('text-align', 'center');
        
        if (end_text != '') {
            card.append(ticker_header, start_header, end_header, body);
        } else {
            card.append(ticker_header, start_header, body);
        }

        var datatable = $('<table>').attr('class', 'datatable' + i + ' table table-striped table-hover table-bordered').attr('style', 'width: 100%; text-align: center;').addClass('display');
        body.append(datatable);

        // 將新創建的元素添加到 card 元素中
        $('#output').append(card, '<br>');

        var tabledata = response[i]['tabledata']

        dt = $('.datatable' + i).DataTable({
            lengthChange: false, // "Show X entries"
            pageLength: 25, // 設置每頁顯示的行數
            paging: false, // 關閉分頁
            data: tabledata,
            columns: [
                { data: 'date', title: '日期' },
                { data: 'low_price', title: '最低價' },
                { data: 'open_price', title: '開盤價' },
                { data: 'profit', title: '未實現收益' },
                { data: 'profit_rate', title: '報酬率(%)' },
            ],
        });
    }
}

function highcharts(series, originalCategories) {
    $('#highcharts_container').empty();
    Highcharts.chart('highcharts_container', {

        title: {
            text: '各股報酬率',
            align: 'left'
        },
    
        yAxis: {
            title: {
                text: '報酬率(%)'
            }
        },
    
        xAxis: {
            type: 'category',
            categories: originalCategories,
            accessibility: {
                rangeDescription: 'date'
            }
        },
    
        legend: {
            layout: 'vertical',
            align: 'right',
            verticalAlign: 'middle'
        },
    
        series: series,
    
        responsive: {
            rules: [{
                condition: {
                    maxWidth: 500
                },
                chartOptions: {
                    legend: {
                        layout: 'horizontal',
                        align: 'center',
                        verticalAlign: 'bottom'
                    }
                }
            }]
        }
    
    });
    
}

function startCounter() {
    let seconds = 0;
    $("#secondsCounter").text(seconds);

    function countSeconds() {
        seconds++;
        $("#secondsCounter").text(seconds);
    }

    // Call countSeconds every second (1000 milliseconds)
    let intervalId = setInterval(countSeconds, 1000);

    // Optionally, you can return the intervalId if you want to be able to stop the counter later
    return intervalId;
}

$(document).ready(function(){
    const loadingContainer = $('#loading-container');
    const loadingbackground = $('#loading-background');
    const secondsCounter = $("#secondsCounter");
    loadingContainer.show();
    loadingbackground.show();
    secondsCounter.show();

    let counterIntervalId = startCounter();

    var formData = {};
    $('select').each(function () {
        formData[this.name] = $(this).val();
    });
    
    $.ajax({
        url: '/stock/ajax_finlabBacktest/', 
        data: formData,
        success: function(response){
            loadingContainer.hide();
            loadingbackground.hide();
            secondsCounter.hide();
            clearInterval(counterIntervalId);

            // 將每個 100 轉換為 null
            var new_highcharts_data = response.highcharts_data.map(item => ({
                name: item.name,
                data: item.data.map(value => value === 100 ? null : value)
            }));

            all_output(response.all_result_data)
            highcharts(new_highcharts_data, response.date_list)
            
        }
    });

    $("select").change(function() {

        loadingContainer.show();
        loadingbackground.show();
        secondsCounter.show();

        let counterIntervalId = startCounter();

        var formData = {};
        $('select').each(function () {
            formData[this.name] = $(this).val();
        });

        var formData = {};
        $('select').each(function () {
            formData[this.name] = $(this).val();
        });

        $.ajax({
            url: '/stock/ajax_finlabBacktest/', 
            data: formData,
            success: function(response){
                loadingContainer.hide();
                loadingbackground.hide();
                secondsCounter.hide();
                clearInterval(counterIntervalId);

                // 將每個100 轉換為 null
                var new_highcharts_data = response.highcharts_data.map(item => ({
                    name: item.name,
                    data: item.data.map(value => value === 100 ? null : value)
                }));

                all_output(response.all_result_data)
                highcharts(new_highcharts_data, response.date_list)
            }
        });
    });
});