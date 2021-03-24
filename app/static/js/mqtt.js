var fan = "";
var lights = "";

document.getElementById('lights').addEventListener('change', function() {
    lights = this.value;
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
  fan = this.value;
  console.log('fan: ', fan);
  fetch("/admin/mqtt/"+room+"/fan/"+fan)
      .then(function (response) {
      return response.json();
      })
      .then(function (message) {
      console.log(message);
  })
});