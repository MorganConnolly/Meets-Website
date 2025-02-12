// Credit: https://www.w3schools.com/howto/howto_js_countdown.asp
function createCountDown(date, id) {
    // Set the date we're counting down to
    var countDownDate = new Date(date).getTime();

    // Update the count down every 1 second
    var x = setInterval(function () {
        // Get today's date and time
        var now = new Date().getTime();

        // Find the distance between now and the count down date
        var distance = countDownDate - now;

        // Time calculations for days, hours, minutes, and seconds
        var days = Math.floor(distance / (1000 * 60 * 60 * 24));
        var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));

        // Display the result in the element with the parameter ID
        document.getElementById(id).innerHTML = days + "d " + hours + "h " + minutes + "m ";

        // If the count down is finished, write some text
        if (distance < 0) {
            clearInterval(x);
            document.getElementById(id).innerHTML = "Meetup Has Begun!";
        }
    }, 1000);
}

function getDay(date, id) {
    const days = ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"]
    const months = ["January","Feburary","March","April","May","June","July","August","September","October","November","December"]

    const d = new Date(date);

    document.getElementById(id).innerHTML = days[d.getDay()] + ", " + ordinal_suffix_of(d.getDate()) + " " + months[d.getMonth()] + " " + d.getFullYear();
}

function reformatDate(date, id) {
    const d = new Date(date);
    console.log(date)
    console.log(d.getDate() + "/" + (d.getMonth() + 1) + "/" + d.getFullYear())
    document.getElementById(id).innerHTML = d.getDate() + "/" + (d.getMonth() + 1) + "/" + d.getFullYear()
}

function getTime(start_date, end_date, id) {
    console.log(id);
    const sd = new Date(start_date);
    const ed = new Date(end_date);
    var start_hours = sd.getHours()
    var start_mins = padMins(sd.getMinutes())
    var end_hours = ed.getHours()
    var end_mins = padMins(ed.getMinutes())

    document.getElementById(id).innerHTML = start_hours + ":" + start_mins + timeSuffix(start_hours) + " to " + end_hours + ":" + end_mins + timeSuffix(end_hours);
}

function padMins(num) {
    if (num < 10) {
        num = num.toString();
        while (num.length < 2) num = "0" + num;
        return num;
    }
    return num;
}

function timeSuffix(hours) {
    if (hours < 12) {
        return "AM";
    }
    return "PM";
}

// Credit: https://stackoverflow.com/questions/13627308/add-st-nd-rd-and-th-ordinal-suffix-to-a-number
function ordinal_suffix_of(i) {
    let j = i % 10,
        k = i % 100;
    if (j === 1 && k !== 11) {
        return i + "st";
    }
    if (j === 2 && k !== 12) {
        return i + "nd";
    }
    if (j === 3 && k !== 13) {
        return i + "rd";
    }
    return i + "th";
}

// Sidebar Functions
// Credit: https://www.youtube.com/watch?v=uy1tgKOnPB0
let btn = document.querySelector("btn")
let sidebar = document.querySelector(".sidebar")

btn.onclick = function () {
    sidebar.classList.toggle("active");
}