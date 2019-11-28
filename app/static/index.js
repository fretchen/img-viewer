Vue.component('image-widget', {
  props: ['image'],
  template: `
  <div class="col-3">
    {{ image.year }} - {{ image.month }} - {{ image.day }}
    <a :href="url" data-toggle="modal" data-target="#exampleModal" data-gallery="example-gallery">
      <img class="img-thumbnail" :src="url"/>
    </a>
    </div>
    `,
    data: function () {
      return {
        url: ''
      }
    },
    mounted: function () {
      this.url = '/cdn/' + this.image.id;
    }
});

Vue.component('image-table', {
  props: ['im_str'],
  template: `
  <div class="row">
  <image-widget v-for="image in images" v-bind:image="image"/>
  <ul>
  </ul>
  </div>
    `,
    data: function () {
      return {
        images: []
      }
    },
    mounted: function () {
      this.images =JSON.parse(this.im_str)
    }
});

var IndexVue = new Vue({
  el: '#imageTable'
})

$(document).on('click', '[data-toggle="modal"]', function(event) {
    var id = $(this).attr('id');
    var address = '/cdn/'+ id;
    $("#modal-img").attr("src",address);
  });
