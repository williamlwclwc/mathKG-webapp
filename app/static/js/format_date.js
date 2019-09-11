
// (1) yyyy-MM-dd
// (2) yyyy/MM/dd
// (3) yyyy-MM-dd hh:mm:ss
// (4) yyyy/MM/dd hh:mm:ss
// (5) hh:mm:ss

// 传入毫秒数和时间格式，输出格式化时间
ms_per_day = 86400000;

function format_Date (date, dateStr, move_d) {
    if(typeof date === "number"){
        var d=new Date();
        d.setTime(date);
        date=d;
    }
    if(move_d !== undefined){
        // date += ms_per_day * move_d;
        var date = new Date(Date.parse(date.toString()) + 86400000 * move_d);
    }


    var arr=dateStr.split(/\/|-|:| /);  //分割字符串,- / : 空格
    var timeArr=[];
    for (var i = 0; i < arr.length; i++) { //按照需要将日期放入数组timeArr
        switch (arr[i]) {
            case "yyyy":
                timeArr.push(date.getFullYear());           
                break;
            case "MM":
                timeArr.push(("0" + (date.getMonth() + 1)).slice(-2));
                break;
            case "dd":
                timeArr.push(("0" + (date.getDate() + 1)).slice(-2));           
                break;
            case "hh":
                timeArr.push(date.getHours());          
                break;
            case "mm":
                timeArr.push(date.getMinutes());        
                break;
            case "ss":
                timeArr.push(date.getSeconds());
                break;
        }
    }
    for (var i = 0; i <arr.length; i++) {
        dateStr = dateStr.replace(arr[i],timeArr[i]);
    }
    return dateStr;
}