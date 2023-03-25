<script setup lang="ts">
import { reactive, computed } from 'vue'
import bingoSheet from '../bingoSheet.json'

interface LooseObject {
  [key: string]: any
}

//HACK God im so lazy. The pics are off by 1 cause i didnt want to write a script to deal with it
let picIndex = 1;
bingoSheet.forEach(x => {
  x.picName = picIndex;
  picIndex++;
})

const state = reactive({
  modal: false,
  tile: {
    tileName: "",
    description: "",
    picName:""
  },
  search: ''
});

function openModal(item: LooseObject):void{
  state.modal = true;
  state.tile.tileName = item.tileName;
  state.tile.description = item.description;
  state.tile.picName = item.picName
}

function closeModal():void{
  state.modal = false;
  state.tile = {
    tileName: "",
    description: "",
    picName:""
  };
}

const filterList = computed(() => {
  if(state.search === ''){
    console.log("test")

    return bingoSheet
  }else{
    console.log("test")
    return bingoSheet.filter(tile => tile.tileName.includes(state.search))
  }
})


</script>

<template>
  <h1>Mega Millions March 2023 Bingo</h1>
  <sub>  This may be the ugliest quickest site i ever made so plz 4give
  </sub>
  <h3>Extra Info</h3>
  <ul style="list-style: none">
    <li>Can be dupe gwd items including nex to cover both tiles</li>
    <li>When posting the screenshots can you please for sets post say 1/4 or 1/6 for metal boots so its easier for us to track. Example on dragon set you get the med helm put 'dragon set 1/4'
    </li>
  </ul>
  <input type="text" placeholder="Search..." v-model="state.search"/>
  <button v-on:click="state.search = ''" >Clear</button>
  <div class="bingo-board">
    <div v-for="(item, index) in filterList" :key="index">
    <div class="bingo-tile" v-on:click="openModal(item)" >
      <!--This code sucks i know but yolo? -->
      <img :src="`./tiles/${item.picName}.png`">

      <!--      <img v-if="index === 0" :src="`./tiles/${index + 1}.png`">-->
<!--      <img v-else-if="index === 71" :src="`./tiles/${index - 1}.png`">-->
<!--      <img v-else :src="`./tiles/${index + 1}.png`">-->
    </div>
    </div>

    <!-- The Modal -->
    <div id="myModal" class="modal" :style="{'display': state.modal ? 'block' : 'none'}"  >

      <!-- Modal content -->
      <div class="modal-content">
        <span class="close" v-on:click="closeModal">&times;</span>
        <p>{{state.tile.tileName}}</p>
        <p>{{state.tile.description}}</p>
      </div>

    </div>

  </div>
</template>

<style scoped>
/* The Modal (background) */
.modal {
  display: none; /* Hidden by default */
  position: fixed; /* Stay in place */
  z-index: 1; /* Sit on top */
  left: 0;
  top: 0;
  width: 100%; /* Full width */
  height: 100%; /* Full height */
  overflow: auto; /* Enable scroll if needed */
  background-color: rgb(0,0,0); /* Fallback color */
  background-color: rgba(0,0,0,0.4); /* Black w/ opacity */
}

/* Modal Content/Box */
.modal-content {
  background-color: #fefefe;
  margin: 15% auto; /* 15% from the top and centered */
  padding: 20px;
  border: 1px solid #888;
  width: 80%; /* Could be more or less, depending on screen size */
}

/* The Close Button */
.close {
  color: #aaa;
  float: right;
  font-size: 28px;
  font-weight: bold;
}

.close:hover,
.close:focus {
  color: black;
  text-decoration: none;
  cursor: pointer;
}
</style>
