Vue.component('image-widget', {
  props: ['image', 'url'],
  template: `
  <div class="col">
    {{ image.year }} - {{ image.month }} - {{ image.day }}
    <a :href="url" data-toggle="modal" data-target="#exampleModal" data-gallery="example-gallery">
      <img class="img-thumbnail" :src="url"/>
    </a>
    </div>
    `
});

var IndexVue = new Vue({
  el: '#imageTable'
})

$(document).on('click', '[data-toggle="modal"]', function(event) {
    var id = $(this).attr('id');
    var address = '/cdn/'+ id;
    $("#modal-img").attr("src",address);
  });
