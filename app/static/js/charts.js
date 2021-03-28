
//occupancy chart
var occupancy = document.getElementById("occupancy").getContext("2d");
var occupancyChart = new Chart(occupancy, {
    type: "bar",
    data: {
    labels: [],
    datasets: [
        {
        label: "Occupancy",
        data: [],
        fill: false,
        backgroundColor: "rgb(157, 128, 209,0.5)",
        lineTension: 0.1,
        },
    ],
    },
    options: {
    scales: {
        xAxes: [
        {
            categoryPercentage: 1.0,
            barPercentage: 1.0,
            type: 'time',
            distribution: 'series'
        },
        ],
        yAxes: [
        {
            ticks: {
            beginAtZero: true,
            callback: function(value) {if (value % 1 === 0) {return value;}},
            },
        },
        ],
    },
    },
});

//temp chart
var temp = document.getElementById("temp").getContext("2d");
var tempChart = new Chart(temp, {
    type: "line",
    data: {
    labels: [],
    datasets: [
        {
        label: "Temperature",
        data: [],
        fill: false,
        borderColor: "rgb(157, 128, 209)",
        lineTension: 0.1,
        },
    ],
    },
    options: {
    scales: {
        xAxes: [
        {
            type: 'time',
            distribution: 'series'
        },
        ],
        yAxes: [
        {
            ticks: {
            beginAtZero: true,
            callback: function(value) {if (value % 1 === 0) {return value;}},
            },
        },
        ],
    },
    },
});

//humid graph
var humid = document.getElementById("humid").getContext("2d");
var humidChart = new Chart(humid, {
    type: "line",
    data: {
    labels: [],
    datasets: [
        {
        label: "Humidity",
        data: [],
        fill: false,
        borderColor: "rgb(157, 128, 209)",
        lineTension: 0.1,
        },
    ],
    },
    options: {
    scales: {
        xAxes: [
        {
            type: 'time',
            distribution: 'series'
        },
        ],
        yAxes: [
        {
            ticks: {
            beginAtZero: true,
            callback: function(value) {if (value % 1 === 0) {return value;}},
            },
        },
        ],
    },
    },
});

//energy graph
var energy = document.getElementById("energy").getContext("2d");
var energyChart = new Chart(energy, {
    type: "line",
    data: {
    labels: [],
    datasets: [
        {
        label: "Energy",
        data: [],
        fill: false,
        borderColor: "rgb(157, 128, 209)",
        lineTension: 0.1,
        },
    ],
    },
    options: {
    scales: {
        xAxes: [
        {
            type: 'time',
            distribution: 'series'
        },
        ],
        yAxes: [
        {
            ticks: {
            beginAtZero: true,
            callback: function(value) {if (value % 1 === 0) {return value;}},
            },
        },
        ],
    },
    },
});



//selector
var temp_room_sensors = ["Occupancy1","Temperature1","Humidity1","Energy1"];
var room_sensors_data = [];
var room_sensors_time = [];
var room = "";

document.getElementById('rooms').addEventListener('change', function() {
    room = this.value;
    console.log('You selected: ', room);

    temp_room_sensors.forEach(function (item, index) {
        room_sensors_data[index] = room.concat(temp_room_sensors[index]) +"_data";
        room_sensors_time[index] = room.concat(temp_room_sensors[index]) +"_time";
      });
    initLiveUpdate()
  });

  
//runs 1st when page is opened
function initLiveUpdate() {
    console.log("reloaded");
    //checks if room selector is empty n chooses 1st room in selector list
    //if (room_sensors_data === undefined || room_sensors_data.length == 0) {
    if ( room === ""){
        room = document.getElementById('rooms').value;
        temp_room_sensors.forEach(function (item, index) {
            room_sensors_data[index] = room.concat(temp_room_sensors[index]) +"_data";
            room_sensors_time[index] = room.concat(temp_room_sensors[index]) +"_time";
          });

        
    }

    fetch("/admin/sql/"+room)
        .then(function (response) {
        return response.json();
        })
        .then(function (data) {
        console.log(data);
        //console.log(room_sensors_data)

        //occupancy
        occupancyChart.data.datasets[0].data = data[room_sensors_data[0]];
        occupancyChart.data.labels = data[room_sensors_time[0]];
        occupancyChart.update();
        if (typeof data[room_sensors_data[0]] === 'undefined'){
            document.getElementById("current_occupancy").innerHTML = 0;
        }else{
            document.getElementById("current_occupancy").innerHTML = data[room_sensors_data[0]][0];
        }
        
        //temperature
        tempChart.data.datasets[0].data = data[room_sensors_data[1]];
        tempChart.data.labels = data[room_sensors_time[1]];
        tempChart.update();
        if (typeof data[room_sensors_data[1]] === 'undefined'){
            document.getElementById("current_temp").innerHTML = 0;
        }else{
            document.getElementById("current_temp").innerHTML = data[room_sensors_data[1]][0];
        }
        //humidity
        humidChart.data.datasets[0].data = data[room_sensors_data[2]];
        humidChart.data.labels = data[room_sensors_time[2]];
        humidChart.update();
        if (typeof data[room_sensors_data[2]] === 'undefined'){
            document.getElementById("current_humid").innerHTML = 0;
        }else{
            document.getElementById("current_humid").innerHTML = data[room_sensors_data[2]][0];
        }
        //energy
        energyChart.data.datasets[0].data = data[room_sensors_data[3]];
        energyChart.data.labels = data[room_sensors_time[3]];
        energyChart.update();
        if (typeof data[room_sensors_data[3]] === 'undefined'){
            document.getElementById("current_energy").innerHTML = 0;
        }else{
            document.getElementById("current_energy").innerHTML = data[room_sensors_data[3]][0];
        }
        })
        .catch(function (error) {
        console.log(error);
        });
    }

if (performance.navigation.type == 0    ||  //navigate
    performance.navigation.type == 1    ||  //reload
    performance.navigation.type == 2 ){     //back_forward


    document.addEventListener("DOMContentLoaded",initLiveUpdate() );
}



//update graphs
function startLiveUpdate() {
    setInterval(function () {
    console.log("fetch");
    fetch("/admin/sql/"+room+"/update")
    // fetch("/admin/mqtt")
        .then(function (response) {
        return response.json();
        })
        .then(function (data) {
        
        
        if(Object.keys(data).length === 0 && data.constructor === Object){
            console.log('no new data')
            return
        }
        

        //occupancy
        if (typeof data[room_sensors_time[0]] !== 'undefined' &&
            typeof occupancyChart.data.labels !== 'undefined'&&
            data[room_sensors_time[0]] !== occupancyChart.data.labels[0]){

                occupancyChart.data.datasets[0].data.unshift(data[room_sensors_data[0]]);
                occupancyChart.data.labels.unshift(data[room_sensors_time[0]]);
                occupancyChart.update();
                if (typeof data[room_sensors_data[0]] === 'undefined'){
                    document.getElementById("current_occupancy").innerHTML = 0;
                }else{
                    document.getElementById("current_occupancy").innerHTML = data[room_sensors_data[0]];
                }           
        }
        //temperature
        if (typeof data[room_sensors_time[1]] !== 'undefined' &&
            typeof tempChart.data.labels !== 'undefined' &&
            data[room_sensors_time[1]] !== tempChart.data.labels[0]){

                tempChart.data.datasets[0].data.unshift(data[room_sensors_data[1]]);
                tempChart.data.labels.unshift(data[room_sensors_time[1]]);
                tempChart.update();
                if (typeof data[room_sensors_data[1]] === 'undefined'){
                    document.getElementById("current_temp").innerHTML = 0;
                }else{
                    document.getElementById("current_temp").innerHTML = data[room_sensors_data[1]];
                }   
        }
        //humidity
        if (typeof data[room_sensors_time[2]] !== 'undefined' &&
            typeof humidChart.data.labels !== 'undefined' &&
            data[room_sensors_time[2]] !== humidChart.data.labels[0]){

                humidChart.data.datasets[0].data.unshift(data[room_sensors_data[2]]);
                humidChart.data.labels.unshift(data[room_sensors_time[2]]);
                humidChart.update(); 
                if (typeof data[room_sensors_data[2]] === 'undefined'){
                    document.getElementById("current_humid").innerHTML = 0;
                }else{
                    document.getElementById("current_humid").innerHTML = data[room_sensors_data[2]];
                }
        }

        //energy
        if (typeof data[room_sensors_time[3]] !== 'undefined' &&
            typeof energyChart.data.labels !== 'undefined' &&
            data[room_sensors_time[3]] !== energyChart.data.labels[0]){
                
                energyChart.data.datasets[0].data.unshift(data[room_sensors_data[3]]);
                energyChart.data.labels.unshift(data[room_sensors_time[3]]);
                energyChart.update();
                if (typeof data[room_sensors_data[3]] === 'undefined'){
                    document.getElementById("current_energy").innerHTML = 0;
                }else{
                    document.getElementById("current_energy").innerHTML = data[room_sensors_data[3]];
                }
        }
        
        })
        .catch(function (error) {
        console.log(error);
        });
    }, 10000);
}




//initialize graph update
startLiveUpdate();




