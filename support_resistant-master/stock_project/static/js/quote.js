// 前端參數調整-的function
function decrease_slider(step, id_slider, id_show) {
    $(id_slider).slider("value", $(id_slider).slider("value") - step);
    $(id_show).val($(id_slider).slider("value"));
}
// 前端參數調整+的function
function increase_slider(step, id_slider, id_show) {
$(id_slider).slider("value", $(id_slider).slider("value") + step);
$(id_show).val($(id_slider).slider("value"));
}
// 定義前端各個參數調整
function slider_settings() {
    $("#slider-range-Vl").slider({
      range: "min",
      value: 5,
      min: 2,
      max: 10,
      slide: function (event, ui) {
        $("#amount_Vl").val(ui.value);
      }
    });
    $("#amount_Vl").val($("#slider-range-Vl").slider("value"));
  
    $("#slider-range-Vr").slider({
      range: "min",
      value: 5,
      min: 2,
      max: 10,
      slide: function (event, ui) {
        $("#amount_Vr").val(ui.value);
      }
    });
    $("#amount_Vr").val($("#slider-range-Vr").slider("value"));
  
    $("#slider-range-Pl").slider({
      range: "min",
      value: 5,
      min: 2,
      max: 10,
      slide: function (event, ui) {
        $("#amount_Pl").val(ui.value);
      }
    });
    $("#amount_Pl").val($("#slider-range-Pl").slider("value"));
  
  
    $("#slider-range-Pr").slider({
      range: "min",
      value: 5,
      min: 2,
      max: 10,
      slide: function (event, ui) {
        $("#amount_Pr").val(ui.value);
      }
    });
    $("#amount_Pr").val($("#slider-range-Pr").slider("value"));
  
    $("#slider-range-swap_times").slider({
      range: "min",
      value: 1,
      min: 0,
      max: 2,
      slide: function (event, ui) {
        $("#swap_times").val(ui.value);
      }
    });
    $("#swap_times").val($("#slider-range-swap_times").slider("value"));
  
    $("#slider-range-close").slider({
      range: "min",
      value: 1,
      min: 1,
      max: 60,
      step: 1,
      slide: function (event, ui) {
        $("#amount_close").val(ui.value);
      }
    });
    $("#amount_close").val($("#slider-range-close").slider("value"));
  
    $("#slider-range-pre").slider({
      range: "min",
      value: 20,
      min: 20,
      max: 300,
      slide: function (event, ui) {
        $("#amount_pre").val(ui.value);
      }
    });
    $("#amount_pre").val($("#slider-range-pre").slider("value"));
  
    $("#slider-range-Time").slider({
      range: "min",
      value: 180,
      min: 120,
      max: 300,
      
      slide: function (event, ui) {
        $("#amount_Time").val(ui.value);
      }
    });
    $("#amount_Time").val($("#slider-range-Time").slider("value"));
  
    $("#slider-range-Gm").slider({
      range: "min",
      value: 1.00,
      min: 0.00,
      max: 3.00,
      step: 0.01,
     
      slide: function (event, ui) {
        $("#amount_Gm").val(ui.value);
      }
    });
    $("#amount_Gm").val($("#slider-range-Gm").slider("value"));
    
    $("#slider-range-NVl").slider({
      range: "min",
      value: 5,
      min: 2,
      max: 20,
      step: 1,
     
      slide: function (event, ui) {
        $("#amount_NVl").val(ui.value);
      }
    });
    $("#amount_NVl").val($("#slider-range-NVl").slider("value"));
  
    $("#slider-range-NVr").slider({
      range: "min",
      value: 5,
      min: 2,
      max: 20,
      step: 1,
     
      slide: function (event, ui) {
        $("#amount_NVr").val(ui.value);
      }
    });
    $("#amount_NVr").val($("#slider-range-NVr").slider("value"));
  
    $("#slider-range-NPl").slider({
      range: "min",
      value: 5,
      min: 2,
      max: 20,
      step: 1,
     
      slide: function (event, ui) {
        $("#amount_NPl").val(ui.value);
      }
    });
    $("#amount_NPl").val($("#slider-range-NPl").slider("value"));
  
    $("#slider-range-NPr").slider({
      range: "min",
      value: 5,
      min: 2,
      max: 20,
      step: 1,
     
      slide: function (event, ui) {
        $("#amount_NPr").val(ui.value);
      }
    });
    $("#amount_NPr").val($("#slider-range-NPr").slider("value"));
  
    $("#slider-range-Nks").slider({
      range: "min",
      value: 90,
      min: 30,
      max: 180,
      step: 1,
     
      slide: function (event, ui) {
        $("#amount_Nks").val(ui.value);
      }
    });
    $("#amount_Nks").val($("#slider-range-Nks").slider("value"));
  
    $("#slider-range-Nke").slider({
      range: "min",
      value: 90,
      min: 30,
      max: 180,
      step: 1,
     
      slide: function (event, ui) {
        $("#amount_Nke").val(ui.value);
      }
    });
    $("#amount_Nke").val($("#slider-range-Nke").slider("value"));
  
    $("#slider-range-Nki").slider({
      range: "min",
      value: 90,
      min: 60,
      max: 180,
      step: 1,
     
      slide: function (event, ui) {
        $("#amount_Nki").val(ui.value);
      }
    });
    $("#amount_Nki").val($("#slider-range-Nki").slider("value"));
  
    $("#slider-range-Nkr").slider({
      range: "min",
      value: 10,
      min: 5,
      max: 80,
      step: 1,
     
      slide: function (event, ui) {
        $("#amount_Nkr").val(ui.value);
      }
    });
    $("#amount_Nkr").val($("#slider-range-Nkr").slider("value"));
  
  }
$(document).ready(function () {
    slider_settings();
});


// 將訊號自動生成radio buttom
function addRadioButtonbuy(labelText, radioButtonId, radioGroupName) {
    // 创建单选按钮元素
    var radioButton = $('<input>').attr({
        type: 'radio',
        value: radioButtonId,
        id: radioButtonId,
        name: radioGroupName // 设置单选按钮的组名，确保只能选择其中一个
    }).addClass('form-check-input').css({
        'font-size': '10px',
    });

    // 创建标签元素
    var label = $('<label>').addClass('form-check-label').text(' ' + labelText).attr('for', radioButtonId);

    // 直接将单选按钮和标签添加到容器中
    $('#radio-container-buy').append(radioButton, label, '<br>');
}
// 將訊號自動生成radio buttom
function addRadioButtonsell(labelText, radioButtonId, radioGroupName) {
    // 创建单选按钮元素
    var radioButton = $('<input>').attr({
        type: 'radio',
        value: radioButtonId,
        id: radioButtonId,
        name: radioGroupName // 设置单选按钮的组名，确保只能选择其中一个
    }).addClass('form-check-input').css({
        'font-size': '10px',
    });

    // 创建标签元素
    var label = $('<label>').addClass('form-check-label').text(' ' + labelText).attr('for', radioButtonId);

    // 直接将单选按钮和标签添加到容器中
    $('#radio-container-sell').append(radioButton, label, '<br>');
}
// 將讀取買訊號
function addScatterSeriesbuy(dataArray) {
    var signalData = [];
    dataArray.forEach(function(dataPoint) {
        var date = dataPoint[0];
        signalData.push([date,1]);
    });

    return signalData;
}
// 將讀取賣訊號
function addScatterSeriessell(dataArray) {
    var signalData = [];
    dataArray.forEach(function(dataPoint) {
        var date = dataPoint[0];
        signalData.push([date, -1]);
    });

    return signalData;
}
// 將線段資料active push上Highchart stock的k線圖上
function createlineactiveSeries(res, datatype,data,obj,color) {
    for (time = 0; time < res[data].length; time++) {
        obj.series.push( {
            showInLegend: false,
            type: datatype,
            color: color,
            data: res[data][time],
            visible: true,
        })
    }
}
// 將線段資料inactive push上Highchart stock的k線圖上
function createlineinactiveSeries(res, datatype,data,obj,color) {
    for (time = 0; time < res[data].length; time++) {
        obj.series.push( {
            showInLegend: false,
            type: datatype,
            color: color,
            data: res[data][time],
            visible: false,
        })
    }
}
// 將方塊條狀資料inactive push上Highchart stock的k線圖上
function createbarinactiveSeries(res, datatype,data,obj,color) {
    for (time = 0; time < res[data].length; time++) {
        obj.series.push( {
            showInLegend: false,
            type: datatype,
            color: color,
            data: res[data][time],
            fillOpacity: 0.3,
            visible: false,
        })
    }
}
// 將方塊條狀資料active push上Highchart stock的k線圖上
function createbaractiveSeries(res, datatype,data,obj,color) {
    for (time = 0; time < res[data].length; time++) {
        obj.series.push( {
            showInLegend: false,
            type: datatype,
            color: color,
            data: res[data][time],
            fillOpacity: 0.8,
            visible: true,
        })
    }
}
// 前端active, inactive 點選時需要重新產生的線段
function checkboxSeriesVisibility(startIndex, endIndex, obj) {
    for (var time = startIndex; time < endIndex; time++) {
        obj.series[time].visible = !obj.series[time].visible;
    }
    Highcharts.stockChart('container', obj).destroy();
    new Highcharts.stockChart('container', obj);
    return true;
}



$(document).ready(function (){
    $('#supres-run').click(function(){
        $("#circle-supres").show();   
        $("#supres-run").hide();
        $("#supres-add_track").hide();
        $("#report-card-supportresistant").hide();
        // 接收前端參數

        var signals_selected_values = [];
        $('.signals-check-input:checked').each(function() {
            signals_selected_values.push($(this).val());
        });
        var start_date = $("#start_date").val();
        var symbol = $("#symbol").val();
        // var email = $("#email").val();
        var peak_left = $("#slider-range-Pl").slider("value");
        var peak_right = $("#slider-range-Pr").slider("value");
        var valley_left = $("#slider-range-Vl").slider("value");
        var valley_right = $("#slider-range-Vr").slider("value");
        var closeness_threshold = $("#slider-range-close").slider("value");
        var swap_times = $("#slider-range-swap_times").slider("value");
        var previous_day = $("#slider-range-pre").slider("value");
        var time_interval = $("#slider-range-Time").slider("value");
        var gap_interval = $("#slider-range-Gm").slider("value");
        var nk_valley_left = $("#slider-range-NVl").slider("value");
        var nk_valley_right = $("#slider-range-NVr").slider("value");
        var nk_peak_left = $("#slider-range-NPl").slider("value");
        var nk_peak_right = $("#slider-range-NPr").slider("value");
        var nk_startdate = $("#slider-range-Nks").slider("value");
        var nk_enddate = $("#slider-range-Nke").slider("value");
        var nk_interval = $("#slider-range-Nki").slider("value");
        var nk_value = $("#slider-range-Nkr").slider("value");
        var support_active = document.getElementById("support_active").checked;
        var support_inactive = document.getElementById("support_inactive").checked;
        var resistance_active = document.getElementById("resistance_active").checked;
        var resistance_inactive = document.getElementById("resistance_inactive").checked;
        var volume_active = document.getElementById("volume_active").checked;
        var volume_inactive = document.getElementById("volume_inactive").checked;
        var gap_up_active = document.getElementById("upgap_active").checked;
        var gap_up_inactive = document.getElementById("upgap_inactive").checked;
        var gap_down_active = document.getElementById("downgap_active").checked;
        var gap_down_inactive = document.getElementById("downgap_inactive").checked;
        var neckline_active = document.getElementById("neckline_active").checked;
        var neckline_inactive = document.getElementById("neckline_inactive").checked;

        var view_block_long_signal = document.getElementById('view_block_long_signal');
        var view_block_short_signal = document.getElementById('view_block_short_signal');
        var view_block_gap = document.getElementById('view_block_gap');
        var view_block_volume = document.getElementById('view_block_volume');
        var view_block_supp_resis = document.getElementById('view_block_supp_resis');
        var view_block_neckline = document.getElementById('view_block_neckline');
        // 設定form格式儲存參數
        var supres_params = new FormData;
        // supres_params.append('email', email);
        supres_params.append('signals_selected_values', signals_selected_values);
        supres_params.append('start_date', start_date);
        supres_params.append('peak_left', peak_left)
        supres_params.append('peak_right', peak_right)
        supres_params.append('valley_left', valley_left)
        supres_params.append('valley_right', valley_right)
        supres_params.append('closeness_threshold', closeness_threshold)
        supres_params.append('swap_times', swap_times)
        supres_params.append('previous_day', previous_day)
        supres_params.append('time_interval', time_interval)
        supres_params.append('gap_interval', gap_interval)
        supres_params.append('nk_valley_left', nk_valley_left)
        supres_params.append('nk_valley_right', nk_valley_right)
        supres_params.append('nk_peak_left', nk_peak_left)
        supres_params.append('nk_peak_right', nk_peak_right)
        supres_params.append('nk_startdate', nk_startdate)
        supres_params.append('nk_enddate', nk_enddate)
        supres_params.append('nk_interval', nk_interval)
        supres_params.append('nk_value', nk_value)
        supres_params.append('symbol', symbol);

        if (view_block_long_signal.style.visibility === 'hidden') {
            view_block_long_signal.style.visibility = '';
        }
        if (view_block_short_signal.style.visibility === 'hidden') {
            view_block_short_signal.style.visibility = '';
        }
        // report表格顯示
        if (view_block_gap.style.visibility === 'hidden') {
            view_block_gap.style.visibility = '';
        }
        if (view_block_volume.style.visibility === 'hidden') {
            view_block_volume.style.visibility = '';
        }
        if (view_block_neckline.style.visibility === 'hidden') {
            view_block_neckline.style.visibility = '';
        }
        if (view_block_supp_resis.style.visibility === 'hidden') {
            view_block_supp_resis.style.visibility = '';
        }
        // active,inactive的checkbox切換
        if (support_active == false) {
          document.getElementById("support_active").checked = true
        }
        if (support_inactive == true) {
            document.getElementById("support_inactive").checked = false
        }
        if (resistance_active == false) {
            document.getElementById("resistance_active").checked = true
        }
        if (resistance_inactive == true) {
            document.getElementById("resistance_inactive").checked = false
        }
        if (volume_active == false) {
            document.getElementById("volume_active").checked = true
        }
        if (volume_inactive == true) {
            document.getElementById("volume_inactive").checked = false
        }
        if (gap_up_active == false) {
            document.getElementById("upgap_active").checked = true
        }
        if (gap_up_inactive == true) {
            document.getElementById("upgap_inactive").checked = false
        }
        if (gap_down_active == false) {
            document.getElementById("downgap_active").checked = true
        }
        if (gap_down_inactive == true) {
            document.getElementById("downgap_inactive").checked = false
        }
        if (neckline_active == false) {
            document.getElementById("neckline_active").checked = true
        }
        if (neckline_inactive == true) {
            document.getElementById("neckline_inactive").checked = false
        }

    //拿到参数后使用Ajax向后提交
    $.ajax({
        url: "/supRes/support_resistant/run_single/",
        type: "post",
        data : supres_params,
        dataType : 'json',
        processData : false,
        contentType : false,
        success: function (res) {
            $("#circle-supres").hide();
            $("#supres-run").show();
            $("#supres-add_track").show();
            $("#report-card-supportresistant").show();
                var ohlc = [];
                var volume = [];
                var gap_table = $('#GapTable').DataTable();
                var volume_table = $('#VolumeTable').DataTable();
                var neckline_table = $('#NecklineTable').DataTable();
                var sup_res_table = $('#SRTable').DataTable();

                gap_table.clear().draw();
                volume_table.clear().draw();
                neckline_table.clear().draw();
                sup_res_table.clear().draw();
                $('#short_signal_table').DataTable().clear().draw();
                $('#long_signal_table').DataTable().clear().draw();

                // show short signals table
                $('#short_signal_table').DataTable({
                    "searching": true,
                    "bAutoWidth": false,
                    "bDestroy": true,
                    "destroy": true,
                    "aLengthMenu":[10, 20, 30],
                    data: res["all_signals"]["Short"],
                    pageLength:10,
                    columns: [
                      { data: "number_of_signals" },
                      { data: "kind" },
                      { data: "status" },
                      { data: "date" },
                      { data: "price" },
                    ],
                    columnDefs:[
                        {
                            targets: [2],
                            createdCell: function (td, cellData, rowData, row, col) {
                                $(td).css('color', 'red')
                            },
                        },
                    ],


                    dom: 'Bfrtip', // 添加 DataTables 按鈕
                    buttons: [
                        {
                            extend: 'excelHtml5',
                            title: "detail of signals",
                            text: "匯出Excel",
                            customize: function (xlsx) {
                            }
                        },
                        'copy',
                        'csv', 
                        'pdf', 
                    ]
                  });

                // show long signals table
                $('#long_signal_table').DataTable({
                    "bAutoWidth": false,
                    "bDestroy": true,
                    "destroy": true,
                    "aLengthMenu":[10, 20, 30],
                    data: res["all_signals"]["Long"],
                    pageLength:10,
                    columns: [
                        { data: "number_of_signals" },
                        { data: "kind" },
                        { data: "status" },
                        { data: "date" },
                        { data: "price" },
                    ],
                    columnDefs:[
                        {
                            targets: [2],
                            createdCell: function (td, cellData, rowData, row, col) {
                                $(td).css('color', 'red')
                            },
                        },
                    ],
                    dom: 'Bfrtip', // 添加 DataTables 按鈕
                    buttons: [
                        {
                            extend: 'excelHtml5',
                            title: "detail of signals",
                            text: "匯出Excel",
                            customize: function (xlsx) {
                            }
                        },
                        'copy',
                        'csv', 
                        'pdf', 
                    ],
                  });
                    
                // gap 的report格式
                if (res['gap_up_active'] != []) {
                    for (var i = 0; i < res['gap_up_active'].length; i++) {
                        var rowData = res['gap_up_active'][i];
                        var row = [
                            res['symbol'],
                            res['stock_data'][res['stock_data'].length - 1][4].toFixed(2),
                            'Up Gap',
                            rowData[0][1],
                            rowData[0][2],
                            moment(rowData[0][0]).format('YYYY-MM-DD'),
                        ];
                        gap_table.row.add(row).draw();
                    }
                }
                if (res['gap_down_active'] != []) {
                    for (var i = 0; i < res['gap_down_active'].length; i++) {
                        var rowData = res['gap_down_active'][i];
                        console.log(rowData[1],'abc')
                        var row = [
                            res['symbol'],
                            res['stock_data'][res['stock_data'].length - 1][4].toFixed(2),
                            'Down Gap',
                            rowData[0][1],
                            rowData[0][2],
                            moment(rowData[0][0]).format('YYYY-MM-DD'),
                        ];
                        gap_table.row.add(row).draw();
                    }
                }
                // volume的report格式
                if (res['bar_report'] != []) {
                    for (var i = 0; i < res['bar_report'].length; i++) {
                        var rowData = res['bar_report'][i];
                        var row = [
                            res['symbol'],
                            res['stock_data'][res['stock_data'].length - 1][4].toFixed(2),
                            moment(rowData[0]).format('YYYY-MM-DD'),
                            rowData[1],
                            rowData[2],
                            moment(rowData[3]).format('YYYY-MM-DD')
                        ];
                        volume_table.row.add(row).draw();
                    }
                }
                // support的report格式
                if (res['support_active'] != []) {
                    for (var i = 0; i < res['support_active'].length; i++) {
                        var rowData = res['support_active'][i];
                        var row = [
                            res['symbol'],
                            res['stock_data'][res['stock_data'].length - 1][4].toFixed(2),
                            'Support',
                            rowData[0][1],
                            moment(rowData[0][0]).format('YYYY-MM-DD'),
                        ];
                        sup_res_table.row.add(row).draw();
                    }
                }
                // resistance的report格式
                if (res['resistance_active'] != []) {
                    for (var i = 0; i < res['resistance_active'].length; i++) {
                        var rowData = res['resistance_active'][i];
                        var row = [
                            res['symbol'],
                            res['stock_data'][res['stock_data'].length - 1][4].toFixed(2),
                            'Resistance',
                            rowData[0][1],
                            moment(rowData[0][0]).format('YYYY-MM-DD'),
                        ];
                        sup_res_table.row.add(row).draw();
                    }
                }
                // neckline的report格式
                if (res['neckline_report'] != []) {
                    for (var i = 0; i < res['neckline_report'].length; i++) {
                        var rowData = res['neckline_report'][i];
                        var row = [
                            res['symbol'],
                            res['stock_data'][res['stock_data'].length - 1][4].toFixed(2),
                            rowData[3],
                            rowData[0],
                            moment(rowData[1]).format('YYYY-MM-DD'),
                            rowData[3],
                        ];
                        neckline_table.row.add(row).draw();
                    }
                }
                dataLength = res['stock_data'].length,

                // set the allowed units for data grouping
                groupingUnits = [[
                    'week',             // unit name
                    [1]               // allowed multiples
                ], [
                    'month',
                    [1, 2, 3, 4, 6]
                ]],

                i = 0;
                for (i; i < dataLength; i += 1) {
                    ohlc.push([
                        res['stock_data'][i][0], // the date
                        res['stock_data'][i][1], // open
                        res['stock_data'][i][2], // high
                        res['stock_data'][i][3], // low
                        res['stock_data'][i][4] // close
                    ]);

                    volume.push([
                        res['stock_data'][i][0], // the date
                        res['volume'][i][1] // the volume
                    ]);
                }
                // 創建Highchart stock 圖
                var obj = {
                    
                    rangeSelector: {
                        selected: 1,
                    },
                    navigator: {
                        series: {
                            color: Highcharts.getOptions().colors[0]
                        }
                    },
                    legend: {
                        align: 'left', //水平方向位置
                        verticalAlign: 'top', //垂直方向位置
                        x: 0, //距离x轴的距离
                        y: 20,
                        enabled: true
                    },

                    xAxis: {
                        title: {
                            text: 'time'
                        }
                    },
                    yAxis: [{
                        labels: {
                            align: 'right',
                            x: -3
                        },
                        title: {
                            text: 'OHLC'
                        },
                        height: '60%',
                        lineWidth: 2,
                        resize: {
                            enabled: true
                        }
                    }, {
                        labels: {
                            align: 'right',
                            x: -3
                        },
                        title: {
                            text: 'Volume'
                        },
                        top: '60%',
                        height: '20%',
                        offset: 0,
                        lineWidth: 2
                    },{
                        labels: {
                            align: 'right',
                            x: -3
                        }, title: {
                            text: 'line'
                        },
                        top: '80%',
                        height: '20%'
                    }],

                    title: {
                        text: res['symbol'] + "  Stock Price",
                    },
                    tooltip: {
                        split: true
                    },
                    series: [{
                        type: 'candlestick',
                        name: 'ohlc',
                        showInLegend: false,
                        data: ohlc,
                        dataGrouping: {
                            units: groupingUnits,
                            enabled: false

                        }
                    }, {
                        type: 'column',
                        showInLegend: false,
                        name: 'volume',
                        data: volume,
                        yAxis: 1,
                        dataGrouping: {
                            units: groupingUnits,
                            enabled: false

                        }
                    }],
                    stockTools: {
                        gui: {
                            /* open/close the buttons by add/remove name in list */
                            /* separator means "-----" in tool bar*/
                            buttons: ['zoomChange', 'fullScreen',
                                'currentPriceIndicator',]
                        }
                    },
                    plotOptions: {
                        candlestick: {
                            color: 'red',
                            upColor: 'green'
                        },
                    }
                }

                createlineactiveSeries(res, 'line','support_active',obj,'#8085e9')
                createlineinactiveSeries(res,'line','support_inactive',obj,'#8085e9')
                createlineactiveSeries(res, 'line','resistance_active',obj,'#e4d354')
                createlineinactiveSeries(res,'line','resistance_inactive',obj,'#e4d354')
                createbaractiveSeries(res,'areasplinerange','bar_active',obj,'#434348')
                createbarinactiveSeries(res,'areasplinerange','bar_inactive',obj,'#434348')
                createbaractiveSeries(res,'areasplinerange','gap_up_active',obj,'#8085e9')
                createbarinactiveSeries(res,'areasplinerange','gap_up_inactive',obj,'#8085e9')
                createbaractiveSeries(res,'areasplinerange','gap_down_active',obj,'#f7a35c')
                createbarinactiveSeries(res,'areasplinerange','gap_down_inactive',obj,'#f7a35c')
                createlineactiveSeries(res, 'line','neckline_support_active',obj,'#8085e9')
                createlineinactiveSeries(res,'line','neckline_support_inactive',obj,'#8085e9')
                createlineactiveSeries(res, 'line','neckline_resistance_active',obj,'#e4d354')
                createlineinactiveSeries(res,'line','neckline_resistance_inactive',obj,'#e4d354')
                Highcharts.stockChart('container', obj);
                var radioButtonContainerbuy=$('#radio-container-buy')
                var radioButtonContainersell=$('#radio-container-sell')
                $('#radio-container-sell').empty();
                $('#radio-container-buy').empty();
                // long
                if (res['gap_up_signal'].length > 0) {
                    addRadioButtonbuy('up gap', 'up_gap','long');
                }
                if (res['big_volume'].length > 0) {
                    addRadioButtonbuy('big volume', 'big_volume_buy','long');
                }
                if (res['resistance_signal'].length > 0) {
                    addRadioButtonbuy('resistance break out', 'resistance','long');
                }
                if (res['neckline_resistance_signal'].length > 0) {
                    addRadioButtonbuy('neckline resistance break out', 'neckline_resistance','long');
                }
                if (res['two_signals_upgap_bar'].length > 0) {
                    addRadioButtonbuy('up gap & big bolume', 'up_gap_big_bolume','long');
                }
                if (res['two_signals_upgap_resistance'].length > 0) {
                    addRadioButtonbuy('up gap & resistance break out', 'up_gap_resistance','long');
                }
                if (res['two_signals_upgap_resistance_neckline'].length > 0) {
                    addRadioButtonbuy('up gap & neckline resistance break out', 'up_gap_neckline_resistance','long');
                }
                if (res['two_signals_bar_resistance'].length > 0) {
                    addRadioButtonbuy('big volume & resistance break out','big volume_resistance','long');
                }
                if (res['two_signals_bar_resistance_neckline'].length > 0) {
                    addRadioButtonbuy('big volume & neckline resistance break out','big volume_neckline_resistance','long');
                }
                if (res['two_signals_resistance_resistance_neckline'].length > 0) {
                    addRadioButtonbuy('resistance break out & neckline resistance break out','resistance_neckline_resistance','long');
                }
                if (res['three_signals_upgap_bar_resistance'].length > 0) {
                    addRadioButtonbuy('up gap & big volume & resistance break out','up_gap_big_volume_resistance','long');
                }
                if (res['three_signals_upgap_bar_resistance_neckline'].length > 0) {
                    addRadioButtonbuy('up gap & resistance break out & neckline resistance break out','up_gap_resistance_neckline_resistance','long');
                }
                if (res['three_signals_bar_resistance_resistance_neckline'].length > 0) {
                    addRadioButtonbuy('big volume & resistance break out & neckline resistance break out',' big volume_resistance_neckline_resistance','long');
                }
                if (res['three_signals_upgap_resistance_resistance_neckline'].length > 0) {
                    addRadioButtonbuy('up gap & resistance break out & neckline resistance break out','up_gap_resistance_neckline_resistance','long');
                }
                if (res['four_signals_buy'].length > 0) {
                    addRadioButtonbuy('all signals',' all_signals');
                }
                radioButtonContainerbuy.show();
                // short
                if (res['gap_down_signal'].length > 0) {
                    addRadioButtonsell('down gap', 'down_gap','short');
                }
                if (res['big_volume'].length > 0) {
                    addRadioButtonsell('big volume', 'big_volume_sell','short');
                }
                if (res['support_signal'].length > 0) {
                    addRadioButtonsell('support break down', 'support','short');
                }
                if (res['neckline_support_signal'].length > 0) {
                    addRadioButtonsell('neckline support break down', 'neckline_support','short');
                }
                if (res['two_signals_downgap_bar'].length > 0) {
                    addRadioButtonsell('down gap & big bolume', 'down_gap_big_bolume','short');
                }
                if (res['two_signals_downgap_support'].length > 0) {
                    addRadioButtonsell('down gap & support break down', 'down_gap_support','short');
                }
                if (res['two_signals_downgap_support_neckline'].length > 0) {
                    addRadioButtonsell('down gap & neckline support break down', 'down_gap_neckline_support','short');
                }
                if (res['two_signals_bar_support'].length > 0) {
                    addRadioButtonsell('big volume & support break down','big volume_support','short');
                }
                if (res['two_signals_bar_support_neckline'].length > 0) {
                    addRadioButtonsell('big volume & neckline support break down','big volume_neckline_support','short');
                }
                if (res['two_signals_support_support_neckline'].length > 0) {
                    addRadioButtonsell('support break down & neckline support break down','support_neckline_support','short');
                }
                if (res['three_signals_downgap_bar_support'].length > 0) {
                    addRadioButtonsell('down gap & big volume & support break down','down_gap_big_volume_support','short');
                }
                if (res['three_signals_downgap_bar_support_neckline'].length > 0) {
                    addRadioButtonsell('down gap & big volume & neckline support break down','down_gap_big_volume_neckline_support','short');
                }
                if (res['three_signals_bar_support_support_neckline'].length > 0) {
                    addRadioButtonsell('big volume & support break down & neckline support break down',' big volume_support_neckline_support','short');
                }
                if (res['three_signals_downgap_support_support_neckline'].length > 0) {
                    addRadioButtonsell('down gap & support break down & neckline support break down','down_gap_support_neckline_support','short');
                }
                if (res['four_signals_sell'].length > 0) {
                    addRadioButtonsell('all signals','all_signals','short');
                }
                var seriesCount_before = obj.series.length;
                radioButtonContainersell.show();

                $("#run_strategy").on("click", function () {
                    Highcharts.stockChart('container', obj);
                    var singal_data=[]
                    var radioContainerbuy = document.getElementById("radio-container-buy");
                    var radioContainersell = document.getElementById("radio-container-sell");
                    var long_signal = [];
                    var short_signal = [];
                    var radioElementsbuy = radioContainerbuy.querySelectorAll("input[type='radio']:checked");
                    var radioElementssell = radioContainersell.querySelectorAll("input[type='radio']:checked");
                    var long_signal = Array.from(radioElementsbuy).map(function(radio) {
                        return radio.nextElementSibling.textContent.trim();
                      });
                    var short_signal = Array.from(radioElementssell).map(function(radio) {
                    return radio.nextElementSibling.textContent.trim();
                    });
                    var signalData = [];
                    // long
                    if (JSON.stringify(long_signal) === JSON.stringify(["up gap"])) {
                        signalData.push(addScatterSeriesbuy(res['gap_up_signal']))
                    }
                    if (JSON.stringify(long_signal) === JSON.stringify(["big volume"])) {
                        signalData.push(addScatterSeriesbuy(res['big_volume']))
                    }
                    if (JSON.stringify(long_signal) === JSON.stringify(["resistance break out"])) {
                        signalData.push(addScatterSeriesbuy(res['resistance_signal']))
                    }
                    if (JSON.stringify(long_signal) === JSON.stringify(["neckline resistance break out"])) {
                        signalData.push(addScatterSeriesbuy(res['neckline_resistance_signal']))
                    }
                    if (JSON.stringify(long_signal) === JSON.stringify(["up gap & big bolume"])) {
                        signalData.push(addScatterSeriesbuy(res['two_signals_upgap_bar']))
                    }
                    if (JSON.stringify(long_signal) === JSON.stringify(["up gap & resistance break out"])) {
                        signalData.push(addScatterSeriesbuy(res['two_signals_upgap_resistance']))
                    }
                    if (JSON.stringify(long_signal) === JSON.stringify(["up gap & neckline resistance break out"])) {
                        signalData.push(addScatterSeriesbuy(res['two_signals_upgap_resistance_neckline']))
                    }
                    if (JSON.stringify(long_signal) === JSON.stringify(["big volume & resistance break out"])) {
                        signalData.push(addScatterSeriesbuy(res['two_signals_bar_resistance']))
                    }
                    if (JSON.stringify(long_signal) === JSON.stringify(["big volume & neckline resistance break out"])) {
                        signalData.push(addScatterSeriesbuy(res['two_signals_bar_resistance_neckline']))
                    }
                    if (JSON.stringify(long_signal) === JSON.stringify(["resistance break out & neckline resistance break out"])) {
                        signalData.push(addScatterSeriesbuy(res['two_signals_resistance_resistance_neckline']))
                    }
                    if (JSON.stringify(long_signal) === JSON.stringify(["up gap & big volume & resistance break out"])) {
                        signalData.push(addScatterSeriesbuy(res['three_signals_upgap_bar_resistance']))
                    }
                    if (JSON.stringify(long_signal) === JSON.stringify(["up gap & big volume & neckline resistance break out"])) {
                        signalData.push(addScatterSeriesbuy(res['three_signals_upgap_bar_resistance_neckline']))
                    }
                    if (JSON.stringify(long_signal) === JSON.stringify(["big volume & resistance break out & neckline resistance break out"])) {
                        signalData.push(addScatterSeriesbuy(res['three_signals_bar_resistance_resistance_neckline']))
                    }
                    if (JSON.stringify(long_signal) === JSON.stringify(["up gap & resistance break out & neckline resistance break out"])) {
                        signalData.push(addScatterSeriesbuy(res['three_signals_upgap_resistance_resistance_neckline']))
                    }
                    if (JSON.stringify(long_signal) === JSON.stringify(["all signals"])) {
                        signalData.push(addScatterSeriesbuy(res['four_signals_buy']))
                    }
                    // short
                    if (JSON.stringify(short_signal) === JSON.stringify(["down gap"])) {
                        signalData.push(addScatterSeriessell(res['gap_down_signal']))
                    }
                    if (JSON.stringify(short_signal) === JSON.stringify(["big volume"])) {
                        signalData.push(addScatterSeriessell(res['big_volume']))
                    }
                    if (JSON.stringify(short_signal) === JSON.stringify(["support break down"])) {
                        signalData.push(addScatterSeriessell(res['support_signal']))
                    }
                    if (JSON.stringify(short_signal) === JSON.stringify(["neckline support break down"])) {
                        signalData.push(addScatterSeriessell(res['neckline_support_signal']))
                    }
                    if (JSON.stringify(short_signal) === JSON.stringify(["down gap & big bolume"])) {
                        signalData.push(addScatterSeriesbuy(res['two_signals_downgap_bar']))
                    }
                    if (JSON.stringify(short_signal) === JSON.stringify(["down gap & support break down"])) {
                        signalData.push(addScatterSeriessell(res['two_signals_downgap_support']))
                    }
                    if (JSON.stringify(short_signal) === JSON.stringify(["down gap & neckline support break down"])) {
                        signalData.push(addScatterSeriessell(res['two_signals_downgap_support_neckline']))
                    }
                    if (JSON.stringify(short_signal) === JSON.stringify(["big volume & support break down"])) {
                        signalData.push(addScatterSeriessell(res['two_signals_bar_support']))
                    }
                    if (JSON.stringify(short_signal) === JSON.stringify(["big volume & neckline support break down"])) {
                        signalData.push(addScatterSeriessell(res['two_signals_bar_support_neckline']))
                    }
                    if (JSON.stringify(short_signal) === JSON.stringify(["support break down & neckline support break down"])) {
                        signalData.push(addScatterSeriessell(res['two_signals_support_support_neckline']))
                    }
                    if (JSON.stringify(short_signal) === JSON.stringify(["down gap & big volume & support break down"])) {
                        signalData.push(addScatterSeriessell(res['three_signals_downgap_bar_support']))
                    }
                    if (JSON.stringify(short_signal) === JSON.stringify(["down gap & big volume & neckline support break down"])) {
                        signalData.push(addScatterSeriessell(res['three_signals_downgap_bar_support_neckline']))
                    }
                    if (JSON.stringify(short_signal) === JSON.stringify(["big volume & support break down & neckline support break down"])) {
                        signalData.push(addScatterSeriessell(res['three_signals_bar_support_support_neckline']))
                    }
                    if (JSON.stringify(short_signal) === JSON.stringify(["down gap & support break down & neckline support break down"])) {
                        signalData.push(addScatterSeriessell(res['three_signals_downgap_support_support_neckline']))
                    }
                    if (JSON.stringify(short_signal) === JSON.stringify(["all signals"])) {
                        signalData.push(addScatterSeriessell(res['four_signals_sell']))
                    }
                    var integratedData = [];
                    var currentSignal = null;
                    var signalDataresults = [].concat(...signalData) //將多維的陣列轉換為一維陣列
                    var signalMap = {};
                    if ((JSON.stringify(long_signal) === JSON.stringify(["big volume"]))&&
                    (JSON.stringify(short_signal) === JSON.stringify(["big volume"]))) {
                        signalDataresults.forEach(function(dataPoint) {
                            var date = dataPoint[0];
                            var signal = dataPoint[1];
                            signalMap[date] = signal;
                        });
                        ohlc.forEach(function(ohlcPoint) {
                            var date = ohlcPoint[0];
                            var signal = signalMap[date];
                            if (signal !== undefined) {
                                currentSignal = 0;
                            } else if (currentSignal === null) {
                                currentSignal = 0;
                            }
                        
                            // 添加整合後的資料到 integratedData 中，包括日期、OHLC 資料和相應的訊號值
                            integratedData.push([date,currentSignal]);
                            
                        });
                        var signal_line = {
                            type: 'line', // 指定圖表類型（這裡使用線性圖表）
                            showInLegend: false,
                            name: 'new-series', // 指定 series 的名稱
                            data: integratedData, // 指定 series 的數據（這裡 newDataArray 是一個包含數據點的陣列）
                            yAxis: 2,// 其他你需要設置的屬性
                            dataGrouping: {
                                units: groupingUnits,
                                enabled: false
    
                            }
                            ,lineWidth: 2
                        };
                        var longSignals = [];
                        var shortSignals = [];
                        var signalDataArray = Object.entries(signalMap).map(function(entry) {
                            var date = parseInt(entry[0]);
                            var signal = entry[1];
                                if (signal === -1) {
                                    shortSignals.push([date, 0]);
                                    longSignals.push([date, 0])
                                }
    
                                return [date, signal];
                                });
                            var longSignalspoint = {
                                type: 'scatter',
                                data: longSignals , // 使用傳遞的數據
                                name: 'Long',
                                marker: {
                                    symbol: 'triangle',
                                    fillColor: 'green',
                                    lineColor: 'green',
                                    lineWidth: 2,
                                    name: 'buy',
                                    enabled: true,
                                    radius: 6
                                },
                                visibility: true,
                                yAxis: 2
                            
                            };
                            var shortSignalspoint = {
                                type: 'scatter',
                                data: shortSignals , // 使用傳遞的數據
                                name: 'Sell',
                                marker: {
                                    symbol: 'triangle-down',
                                    fillColor: 'red',
                                    lineColor: 'red',
                                    lineWidth: 2,
                                    name: 'sell',
                                    enabled: true,
                                    radius: 6
                                },
                                visibility: true,
                                yAxis: 2
                            
                            };
                    }
                    else  {
                    signalDataresults.forEach(function(dataPoint) {
                        var date = dataPoint[0];
                        var signal = dataPoint[1];
                        signalMap[date] = signal;
                    });
                    ohlc.forEach(function(ohlcPoint) {
                        var date = ohlcPoint[0];
                        var signal = signalMap[date];
                        if (signal !== undefined) {
                            currentSignal = signal;
                        } else if (currentSignal === null) {
                            currentSignal = 0;
                        }
                    
                        // 添加整合後的資料到 integratedData 中，包括日期、OHLC 資料和相應的訊號值
                        integratedData.push([date,currentSignal]);
                        
                    });
                    
                    var signal_line = {
                        type: 'line', // 指定圖表類型（這裡使用線性圖表）
                        showInLegend: false,
                        name: 'new-series', // 指定 series 的名稱
                        data: integratedData, // 指定 series 的數據（這裡 newDataArray 是一個包含數據點的陣列）
                        yAxis: 2,// 其他你需要設置的屬性
                        dataGrouping: {
                            units: groupingUnits,
                            enabled: false

                        }
                        ,lineWidth: 2
                    };
                    var longSignals = [];
                    var shortSignals = [];
                    var signalDataArray = Object.entries(signalMap).map(function(entry) {
                        var date = parseInt(entry[0]);
                        var signal = entry[1];
                            if (signal === 1) {
                                longSignals.push([date, signal]);
                            } else if (signal === -1) {
                                shortSignals.push([date, signal]);
                            }

                            return [date, signal];
                        });
                        var longSignalspoint = {
                            type: 'scatter',
                            data: longSignals , // 使用傳遞的數據
                            name: 'Long',
                            marker: {
                                symbol: 'triangle',
                                fillColor: 'green',
                                lineColor: 'green',
                                lineWidth: 2,
                                name: 'buy',
                                enabled: true,
                                radius: 6
                            },
                            visibility: true,
                            yAxis: 2
                        
                        };
                        var shortSignalspoint = {
                            type: 'scatter',
                            data: shortSignals , // 使用傳遞的數據
                            name: 'Sell',
                            marker: {
                                symbol: 'triangle-down',
                                fillColor: 'red',
                                lineColor: 'red',
                                lineWidth: 2,
                                name: 'sell',
                                enabled: true,
                                radius: 6
                            },
                            visibility: true,
                            yAxis: 2
                        
                        };
                    }
                    var seriesCount_after= obj.series.length;
                    if ((seriesCount_after-seriesCount_before) ==3){
                        obj.series.splice(seriesCount_after - 3, 3)
                    }
                    // 將新的 series 物件添加到 obj 的 series 陣列中
                    obj.series.push(signal_line);
                    obj.series.push(longSignalspoint);
                    obj.series.push(shortSignalspoint);
                    Highcharts.stockChart('container', obj)
                    })
                $("#support_active").on("click", function () {
                    checkboxSeriesVisibility(2, 2 + res['support_active'].length, obj);
                });
                $("#support_inactive").on("click", function () {
                    checkboxSeriesVisibility( 
                    2 + res['support_active'].length,
                    res['support_active'].length + res['support_inactive'].length + 2, 
                    obj);
                });
                $("#resistance_active").on("click", function () {
                    checkboxSeriesVisibility( 
                    res['support_active'].length + res['support_inactive'].length + 2,
                    res['support_active'].length + res['support_inactive'].length + 2 + res['resistance_active'].length, 
                    obj);
                });
                $("#resistance_inactive").on("click", function () {
                    checkboxSeriesVisibility( 
                    res['support_active'].length + res['support_inactive'].length + res['resistance_active'].length + 2,
                    res['support_active'].length + res['support_inactive'].length + 2 + res['resistance_active'].length + res['resistance_inactive'].length, 
                    obj);
                });
                $("#volume_active").on("click", function () {
                    checkboxSeriesVisibility( 
                    res['support_active'].length + res['support_inactive'].length + res['resistance_active'].length + res['resistance_inactive'].length + 2,
                    res['support_active'].length + res['support_inactive'].length + 2 + res['resistance_active'].length + res['resistance_inactive'].length + res['bar_active'].length,
                    obj);
                });
                $("#volume_inactive").on("click", function () {
                    checkboxSeriesVisibility( 
                    res['support_active'].length + res['support_inactive'].length + res['resistance_active'].length + res['resistance_inactive'].length + res['bar_active'].length +2,
                    res['support_active'].length + res['support_inactive'].length + 2 + res['resistance_active'].length + res['resistance_inactive'].length + res['bar_active'].length + res['bar_inactive'].length,
                    obj);
                });
                $("#upgap_active").on("click", function () {
                    checkboxSeriesVisibility( 
                    res['support_active'].length + res['support_inactive'].length + res['resistance_active'].length + res['resistance_inactive'].length + res['bar_active'].length + res['bar_inactive'].length + 2,
                    res['support_active'].length + res['support_inactive'].length + 2 + res['resistance_active'].length + res['resistance_inactive'].length + res['bar_active'].length + res['bar_inactive'].length + res['gap_up_active'].length,
                    obj);
                });
                $("#upgap_inactive").on("click", function () {
                    checkboxSeriesVisibility( 
                    res['support_active'].length + res['support_inactive'].length + res['resistance_active'].length + res['resistance_inactive'].length+
                    res['bar_active'].length + res['bar_inactive'].length + res['gap_up_active'].length+2,
                    res['support_active'].length + res['support_inactive'].length + 2 + res['resistance_active'].length + res['resistance_inactive'].length +
                    res['bar_active'].length + res['bar_inactive'].length + res['gap_up_active'].length+res['gap_up_inactive'].length,
                    obj);
                });
                $("#downgap_active").on("click", function () {
                    checkboxSeriesVisibility( 
                    res['support_active'].length + res['support_inactive'].length + res['resistance_active'].length + res['resistance_inactive'].length + res['bar_active'].length + res['bar_inactive'].length + 
                    res['gap_up_active'].length+ res['gap_up_inactive'].length+2,
                    res['support_active'].length + res['support_inactive'].length + 2 + res['resistance_active'].length + res['resistance_inactive'].length + res['bar_active'].length + res['bar_inactive'].length + 
                    res['gap_up_active'].length+ res['gap_up_inactive'].length+res['gap_down_active'].length,
                    obj);
                });
                $("#downgap_inactive").on("click", function () {
                    checkboxSeriesVisibility( 
                    res['support_active'].length + res['support_inactive'].length + res['resistance_active'].length + res['resistance_inactive'].length + res['bar_active'].length + res['bar_inactive'].length + 
                    res['gap_up_active'].length+res['gap_up_inactive'].length+res['gap_down_active'].length+2,
                    res['support_active'].length + res['support_inactive'].length + 2 + res['resistance_active'].length + res['resistance_inactive'].length + res['bar_active'].length + res['bar_inactive'].length + 
                    res['gap_up_active'].length+res['gap_up_inactive'].length+res['gap_down_active'].length+res['gap_down_inactive'].length,
                    obj);
                });
                $("#neckline_active").on("click", function () {
                    checkboxSeriesVisibility( 
                    res['support_active'].length + res['support_inactive'].length + res['resistance_active'].length + res['resistance_inactive'].length + res['bar_active'].length + res['bar_inactive'].length + 
                    res['gap_up_active'].length + res['gap_up_inactive'].length + res['gap_down_active'].length +res['gap_down_inactive'].length+ 2,
                    res['support_active'].length + res['support_inactive'].length + 2 + res['resistance_active'].length + res['resistance_inactive'].length + res['bar_active'].length + res['bar_inactive'].length + 
                    res['gap_up_active'].length + res['gap_up_inactive'].length + res['gap_down_active'].length + res['gap_down_inactive'].length+res['neckline_support_active'].length,
                    obj);
                });
                $("#neckline_active").on("click", function () {
                    checkboxSeriesVisibility( 
                    res['support_active'].length + res['support_inactive'].length + res['resistance_active'].length + res['resistance_inactive'].length + res['bar_active'].length + res['bar_inactive'].length + 
                    res['gap_up_active'].length + res['gap_up_inactive'].length + res['gap_down_active'].length +res['gap_down_inactive'].length+res['neckline_support_active'].length+res['neckline_support_inactive'].length+ 2,
                    res['support_active'].length + res['support_inactive'].length + 2 + res['resistance_active'].length + res['resistance_inactive'].length + res['bar_active'].length + res['bar_inactive'].length + 
                    res['gap_up_active'].length + res['gap_up_inactive'].length + res['gap_down_active'].length + res['gap_down_inactive'].length+res['neckline_support_active'].length+res['neckline_support_inactive'].length+res['neckline_resistance_active'].length,
                    obj);
                });
                $("#neckline_inactive").on("click", function () {
                    checkboxSeriesVisibility( 
                    res['support_active'].length + res['support_inactive'].length + res['resistance_active'].length + res['resistance_inactive'].length + res['bar_active'].length + res['bar_inactive'].length + 
                    res['gap_up_active'].length + res['gap_up_inactive'].length + res['gap_down_active'].length +res['gap_down_inactive'].length+res['neckline_support_active'].length+ 2,
                    res['support_active'].length + res['support_inactive'].length + 2 + res['resistance_active'].length + res['resistance_inactive'].length + res['bar_active'].length + res['bar_inactive'].length + 
                    res['gap_up_active'].length + res['gap_up_inactive'].length + res['gap_down_active'].length + res['gap_down_inactive'].length+res['neckline_support_active'].length+res['neckline_support_inactive'].length,
                    obj);
                });
                $("#neckline_inactive").on("click", function () {
                    checkboxSeriesVisibility( 
                    res['support_active'].length + res['support_inactive'].length + res['resistance_active'].length + res['resistance_inactive'].length + res['bar_active'].length + res['bar_inactive'].length + 
                    res['gap_up_active'].length + res['gap_up_inactive'].length + res['gap_down_active'].length +res['gap_down_inactive'].length+res['neckline_support_active'].length+res['neckline_support_inactive'].length+res['neckline_resistance_active'].length+ 2,
                    res['support_active'].length + res['support_inactive'].length + 2 + res['resistance_active'].length + res['resistance_inactive'].length + res['bar_active'].length + res['bar_inactive'].length + 
                    res['gap_up_active'].length + res['gap_up_inactive'].length + res['gap_down_active'].length + res['gap_down_inactive'].length+res['neckline_support_active'].length+res['neckline_support_inactive'].length+res['neckline_resistance_active'].length+res['neckline_resistance_inactive'].length,
                    obj);
                });
            }
        });         
    });

    $('#supres-add_track').click(function(){
        var signals_selected_values = [];
        $('.signals-check-input:checked').each(function() {
            signals_selected_values.push($(this).val());
        });
        var start_date = $("#start_date").val();
        var symbol = $("#symbol").val();
        // var email = $("#email").val();
        var peak_left = $("#slider-range-Pl").slider("value");
        var peak_right = $("#slider-range-Pr").slider("value");
        var valley_left = $("#slider-range-Vl").slider("value");
        var valley_right = $("#slider-range-Vr").slider("value");
        var closeness_threshold = $("#slider-range-close").slider("value");
        var swap_times = $("#slider-range-swap_times").slider("value");
        var previous_day = $("#slider-range-pre").slider("value");
        var time_interval = $("#slider-range-Time").slider("value");
        var gap_interval = $("#slider-range-Gm").slider("value");
        var nk_valley_left = $("#slider-range-NVl").slider("value");
        var nk_valley_right = $("#slider-range-NVr").slider("value");
        var nk_peak_left = $("#slider-range-NPl").slider("value");
        var nk_peak_right = $("#slider-range-NPr").slider("value");
        var nk_startdate = $("#slider-range-Nks").slider("value");
        var nk_enddate = $("#slider-range-Nke").slider("value");
        var nk_interval = $("#slider-range-Nki").slider("value");
        var nk_value = $("#slider-range-Nkr").slider("value");
        // 設定form格式儲存參數
        var supres_params = new FormData;
        // supres_params.append('email', email);
        supres_params.append('signals_selected_values', signals_selected_values);
        supres_params.append('start_date', start_date);
        supres_params.append('peak_left', peak_left);
        supres_params.append('peak_right', peak_right);
        supres_params.append('valley_left', valley_left);
        supres_params.append('valley_right', valley_right);
        supres_params.append('closeness_threshold', closeness_threshold);
        supres_params.append('swap_times', swap_times);
        supres_params.append('previous_day', previous_day);
        supres_params.append('time_interval', time_interval);
        supres_params.append('gap_interval', gap_interval);
        supres_params.append('nk_valley_left', nk_valley_left);
        supres_params.append('nk_valley_right', nk_valley_right);
        supres_params.append('nk_peak_left', nk_peak_left);
        supres_params.append('nk_peak_right', nk_peak_right);
        supres_params.append('nk_startdate', nk_startdate);
        supres_params.append('nk_enddate', nk_enddate);
        supres_params.append('nk_interval', nk_interval);
        supres_params.append('nk_value', nk_value);
        supres_params.append('symbol', symbol);

        //add_track Ajax
        $.ajax({
            url: "/supRes/monitor/add_track/",
            type: "post",
            data : supres_params,
            dataType : 'json',
            processData : false,
            contentType : false,
            success: function (res) {
                alert(res["message"]);
            }
        });
    });
})             
        