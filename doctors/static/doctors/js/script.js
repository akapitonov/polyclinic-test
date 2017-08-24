function getDate(dt){
    var year = dt.getFullYear(),
        mounth = (dt.getMonth() < 10) ? '0' + (dt.getMonth() + 1): (dt.getMonth() + 1),
        day = (dt.getDate() < 10) ? '0' + dt.getDate(): dt.getDate();
    return year + '-' + mounth + '-' + day;
}

function disableDates(picker, $records){
    var dates_busy = Object.keys($records);
    var disabledDates = [];
    for(var index in dates_busy) {
        var allowTimes = $records[dates_busy[index]];
        if (allowTimes.length === 0){
            disabledDates.push(dates_busy[index].toString())
        }
    }
    picker.setOptions({
        disabledDates: disabledDates, formatDate:'Y-m-d'
    });
}


$(function() {
    var $records = $('.records').data('records');
    $records = JSON.parse(JSON.stringify($records));
    $.datetimepicker.setLocale('ru');
    $('input[name="1-date_record"]').datetimepicker({
        dayOfWeekStart: 1,
        allowTimes: $records['all'],
        disabledWeekDays: [0, 6],
        defaultDate:'+1970/01/02',
        format: 'Y-m-d H:00',
        minDate:'-1970/01/01',
        onShow:function(ct, $i) {
          disableDates(this, $records);
        },
        onChangeDateTime:function(ct,$i){
            this.setOptions({allowTimes:$records['all']});
            var dt = getDate(ct);
            var dates_busy = Object.keys($records);
            for(var index in dates_busy){
                if (dates_busy[index] === dt){
                    var allowTimes = $records[dates_busy[index]];

                    if (allowTimes.length === 0){
                        this.setOptions({disabledDates: [dt], formatDate:'Y-m-d'})
                    }
                    else {
                        this.setOptions({allowTimes: allowTimes});
                    }
                    break;
                }
            }
        }
    });
});