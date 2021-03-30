var fan;
var lights;

document.getElementById('lights').addEventListener('change', function() {
    if (this.value === "OFF"){
      lights = 0;
    }else if(this.value === "ON"){
      lights = 1;
    }

    console.log('lights: ', lights);

    fetch("/admin/mqtt/"+room+"/lights/"+lights)
        .then(function (response) {
        return response.json();
        })
        .then(function (message) {
        console.log(message);
    })
  });

document.getElementById('fan').addEventListener('change', function() {
  if (this.value === "OFF"){
    fan = 0;
  }else if(this.value === "ON"){
    fan = 1;
  }
  console.log('fan: ', fan);
  fetch("/admin/mqtt/"+room+"/fan/"+fan)
      .then(function (response) {
      return response.json();
      })
      .then(function (message) {
      console.log(message);
  })
});