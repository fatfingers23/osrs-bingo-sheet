<script setup lang="ts">
import {reactive, computed} from 'vue'
import bingoSheet from '../bingoSheet.json'
// eslint-disable-next-line no-undef
// import Papa from 'papaparse'
// import { useRoute } from 'vue-router'
interface LooseObject {
  [key: string]: any
}

const reactiveBingo = reactive(bingoSheet);


//HACK God im so lazy. The pics are off by 1 cause i didnt want to write a script to deal with it
let picIndex = 1;
reactiveBingo.forEach(x => {
  x.picName = picIndex;
  picIndex++;
})

const state = reactive({
  modal: false,
  tile: {
    tileName: "",
    description: "",
    picName: ""
  },
  search: ''
});


document.addEventListener('keyup', function (evt) {
  if (evt.key === 'Escape') {
    closeModal()
  }
});

function openModal(item: LooseObject): void {
  state.modal = true;
  state.tile.tileName = item.tileName;
  state.tile.description = item.description;
  state.tile.picName = item.picName
}

function closeModal(): void {
  state.modal = false;
  state.tile = {
    tileName: "",
    description: "",
    picName: ""
  };
}

const filterList = computed(() => {
  if (state.search === '') {
    return reactiveBingo
  } else {
    return reactiveBingo.filter(tile => tile.tileName.toLowerCase().includes(state.search.toLowerCase()))
  }
})

// const route = useRoute()
// const teamName = route.params.teamName;
//
//
// if(teamName){
//   fetch("")
//       .then(x => x.text().then(
//           gsheet => {
//             const parsedSheet = Papa.parse(gsheet, {header:true});
//             parsedSheet.data.forEach(row => {
//               const drop = row['Drops'];
//               let tile = reactiveBingo.find(x => x.tileName.toLowerCase() === drop.toLowerCase())
//               if(tile){
//
//                 tile.complete = row[teamName] == 1;
//               }
//             })
//           }
//       ))
// }


</script>

<template>

  <h1>April showers, bring flash bingos </h1>

<!--  <h2>Team: {{teamName}}</h2>-->
  <h3>Extra Info</h3>
  <p>
      1m entry for your first raffle ticket.
      +1 ticket for every bingo tile you earn, 16 tiles total to gain!

      Three raffle prizes provided by the clan. However, more entries = more prizes! (Each member limited to one prize)
      PRIZES:
      1. Armadyl Godsword
      2. Elder Maul
      3. Dragonfire Ward

      This is a SOLO event.
      Bingo sheet will be released an hour before event.
      Keyword will be posted at the start of the event.
      Screenshots of items need to be posted in #botw-drops with the keyword visible.
      Strongly encourage using WOM to display keyword when screenshotting drops. Feel free to contact me or other mods with any questions you may have.
      I will do a live wheel spin in one of the voice chat channels to determine raffle winners for prizes.
      I will do a live wheel spin in one of the voice chat channels to determine raffle winners for prizes.
  </p>
  <div style="padding-bottom: 10px">
    <input type="text" placeholder="Search..." v-model="state.search"/>
    <button v-on:click="state.search = ''">Clear</button>
  </div>
  <div class="bingo-board">
    <div v-for="(item, index) in filterList" :key="index">
      <div v-if="item.complete" class="bingo-tile done">
<!--        <img :src="`./tiles/${item.picName}.png`">-->

        <div class="tile-text">{{item.tileName}}</div>
      </div>

      <div v-else class="bingo-tile" v-on:click="openModal(item)">
        <img :src="`./tiles/${item.picName}.png`">
      </div>
    </div>

    <!-- The Modal -->
    <div id="myModal" class="modal" :style="{'display': state.modal ? 'block' : 'none'}">

      <!-- Modal content -->
      <div class="modal-content">
        <span class="close" v-on:click="closeModal">&times;</span>
        <p>{{ state.tile.tileName }}</p>
        <p>{{ state.tile.description }}</p>
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
  background-color: rgb(0, 0, 0); /* Fallback color */
  background-color: rgba(0, 0, 0, 0.4); /* Black w/ opacity */
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

.done {
  background: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' version='1.1' preserveAspectRatio='none' viewBox='0 0 100 100'><path d='M100 0 L0 100 ' stroke='black' stroke-width='1'/><path d='M0 0 L100 100 ' stroke='black' stroke-width='1'/></svg>");
  background-repeat:no-repeat;
  background-position:center center;
  background-size: 100% 100%, auto;
  z-index: 1000000;
  color: red;

}
</style>
