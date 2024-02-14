<script setup lang="ts" xmlns:x-transition="http://www.w3.org/1999/xhtml">
import {reactive, computed} from 'vue'
import bingoSheet from '../bingoSheet.json'
// eslint-disable-next-line no-undef
import Papa from 'papaparse'
import {useRoute} from 'vue-router'

interface LooseObject {
  [key: string]: any
}

const checkMarkImage = "check-mark-icon-png.webp";

const reactiveBingo = reactive(bingoSheet);

let picIndex = 0;
reactiveBingo.forEach(x => {
  x.picName = picIndex.toString();
  picIndex++;
});

reactiveBingo.forEach(x => {
  x.tileName = x.tileName.replace(/[\/']/g, "").replace(/ /g, "_").toUpperCase();
});

reactiveBingo.forEach(x => {
  x.numberDropsRequired = 1;
});

reactiveBingo.forEach(x => {
  x.portionCompleted = "0";
});

const state = reactive({
  modal: false,
  tile: {
    tileName: "",
    description: "",
    picName: "",
    portionCompleted: ""
  },
  search: '',
  teamName: '',
  totalComplete: computed(() => {
    return reactiveBingo.filter(x => x.complete).length
  })
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
  state.tile.picName = item.picName;
  state.tile.portionCompleted = item.portionCompleted;
}

function closeModal(): void {
  state.modal = false;
  state.tile = {
    tileName: "",
    description: "",
    picName: "",
    portionCompleted: ""
  };
}

const filterList = computed(() => {
  if (state.search === '') {
    return reactiveBingo
  } else {
    return reactiveBingo.filter(tile => tile.tileName.toLowerCase().includes(state.search.toLowerCase()))
  }
})

const route = useRoute()
const passcode = route.params.passcode;


const getCheckedTiles = () => {
	fetch("/teams-tiles")
		.then(response => {
			return response.json() as Promise<{ tiles: any}>;
		})
		.then((tiles: any) => {
			let i = 0;
			Object.entries(tiles).forEach(tile => {
				let name: string;
				let value: number;
				// @ts-ignore
				[name, value] = tile;

				if (reactiveBingo[i] && name !== "TeamName") {
                	const bingoTile = reactiveBingo.find(x => x.tileName === name);
                	if (bingoTile) {
						// @ts-ignore
                		if (value >= parseInt(bingoTile.numberDropsRequired)) {
                			bingoTile.complete = true;
                		} else {
                  			bingoTile.portionCompleted = value.toString();
						}
                	}
              }

              i++;

			});
		});
};

getCheckedTiles();

const start = new Date("2024-02-16T18:00:00Z")
const end = new Date("2024-02-26T00:00:00Z")
</script>

<template>


  <div class="p-3">

    <div class="text-center mt-10">
      <h1 class="text-3xl">Insomniacs vs Hurt B-I-N-G-O</h1>
      <span class="text-1xl font-bold">{{start.toLocaleString()}} till {{end.toLocaleString()}}</span>
    </div>
    <div class="text-center mt-3 mb-2">
      <h1 class="text-3xl" v-show="state.teamName != ''">Team: {{ state.teamName}}</h1>
      <h1 class="text-3xl" v-show="state.totalComplete !== 0">Total Tiles Completed: {{ state.totalComplete }}</h1>
    </div>

<!--    <div class="text-center mt-3">-->
<!--      <h3 class="text-2xl">Extra Info</h3>-->
<!--    </div>-->
<!--    <div class="p-6 md:p-10">-->
<!--      <p class="">-->

<!--Do we want anything here?-->
<!--      </p>-->

<!--      <p>-->

<!--      </p>-->
<!--    </div>-->
    <div class="flex justify-center">
      <div class="form-control ">
        <div class="input-group ">
          <input type="text" placeholder="Search…" class="input input-bordered " v-model="state.search"/>
          <button class="btn btn-square" v-on:click="state.search = ''">
            X
          </button>
        </div>
      </div>
    </div>
    <div class="md:p-10 p-5 grid gap-2 md:gap-4 grid-cols-4 grid-rows-2 md:grid-cols-8 md:grid-rows-4">
      <div v-for="(item, index) in filterList" :key="index">

        <div v-if="item.complete" class="bingo-tile done" v-on:click="openModal(item)">
          <img :src="`${checkMarkImage}`" class="check-mark">
          <img :src="`./tiles/${item.picName}.png`" class="tile-image">
        </div>

        <div v-else class="bingo-tile text-center" v-on:click="openModal(item)">
          <img :src="`./tiles/${item.picName}.png`">
          <span v-if="item.portionCompleted !== '0'" class="tile-text ">{{ item.portionCompleted }}</span>
        </div>
      </div>


    </div>

    <!-- The Modal -->
    <Transition name="fade">

      <div
          class="fixed inset-0 w-full h-full z-20 bg-black bg-opacity-50 duration-300 overflow-y-auto"
          v-show="state.modal"

      >
        <div v-show="state.modal"
             class="relative lg:w-1/2 mx-2 sm:mx-auto my-10 opacity-100">
          <div class="modal-show" id="my-modal-2">
            <div class="modal-box">
              <h3 class="font-bold text-lg">{{ state.tile.tileName }}</h3>
              <p class="py-4">{{ state.tile.description }}</p>
              <div class="flex justify-center text-center">
                <img :src="`./tiles/${state.tile.picName}.png`" alt="bingo tile">

              </div>
              <div v-show="state.tile.portionCompleted" class="text-center">
                <p v-if="state.tile.portionCompleted !== '0'">{{ state.tile.portionCompleted }}</p>
              </div>
              <div class="modal-action">
                <button v-on:click="closeModal" class="btn">close</button>
              </div>
            </div>
          </div>

        </div>
      </div>
    </Transition>


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
  width: 100%;
  height: auto;
  position: relative;
  top: 0;
  left: 0;
  //background: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' version='1.1' preserveAspectRatio='none' viewBox='0 0 100 100'><path d='M100 0 L0 100 ' stroke='black' stroke-width='1'/><path d='M0 0 L100 100 ' stroke='black' stroke-width='1'/></svg>");
  //background-repeat: no-repeat;
  //background-position: center center;
//background-size: 100% 100%, auto; z-index: 1000000; position: relative; //color: red; cursor: pointer;
}

.done .tile-image {
  position: relative;
  "-webkit-filter": grayscale(1);
  filter: grayscale(1);
  z-index: 1;
  max-width: 100%;
}

.done .check-mark {
  position: absolute;
  z-index: 3;
  max-width: 50%;
  max-height: 50%
}

.bingo-tile {
  cursor: pointer;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}
</style>
