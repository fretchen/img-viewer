Vue.component('image-widget', {
  props: ['image'],
  template: `
  <div class="col-3">
    {{ image.year }} - {{ image.month }} - {{ image.day }}

    <img class="img-thumbnail" :src="url" v-on:click="showModal = !showModal"/>

    <b-modal no-fade="true" hide-footer="true" v-model="showModal">
    <img class="img-fluid" :src="url"/>
    </b-modal>
    </div>
    `,
    data: function () {
      return {
        url: '',
        showModal: false
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
});
