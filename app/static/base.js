Vue.component('machine-selector', {
  props: ['machines', 'selected'],
  template: `
  <div class="form-inline">
  <label class="col-form-label">  Experiment:</label>
  <div class="col-auto">
  <select class="form-control" v-model='selected'>
  <option v-for="machine in machines">{{ machine }}</option>
  </select>
  </div>
  <div class="col-auto" >
  <button class="btn btn-primary " v-on:click='greet'>Select</button>
  </div>
  </div>
  `,
  methods: {
    greet: function (event) {
      // `this` inside methods points to the Vue instance
      var address = '/machine/' + this.selected;
      location.href = address;
      // `event` is the native DOM event
    }
  }
})

var machineSubmit = new Vue({
  el: '#selectMachine',
  data: {
    selected: $("#machineSelected").text()
  }
})

$('#datepicker').datepicker({
  format: "yyyy-mm-dd",
  clearBtn: true,
  keyboardNavigation: false,
  forceParse: false,
  autoclose: true,
  todayHighlight: true
});

$( "#submit" ).click(function() {
  var start = $("#start").val();
  var end = $("#end").val();
  var machine = $("#machineSelected").text();
  var address = '/machine/'+ machine +'/dates/' + start + '/' + end;
  location.href = address;
});
