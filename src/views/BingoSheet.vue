<script setup lang="ts" xmlns:x-transition="http://www.w3.org/1999/xhtml">
import {reactive, computed, onMounted, ref} from 'vue'
// eslint-disable-next-line no-undef
import Papa from 'papaparse'
import {useRoute} from 'vue-router'

interface LooseObject {
  [key: string]: any
}

type BingoTile = {
  tileName: string,
  description: string,
  picName: string,
  complete: boolean,
  portionCompleted: string
}


const reactiveBingo = ref([] as BingoTile[]);
const reactiveGSheet = ref([] as LooseObject[]);

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
    return reactiveBingo.value.filter(x => x.complete).length
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
    return reactiveBingo.value
  } else {
    return reactiveBingo.value.filter(tile => tile.tileName.toLowerCase().includes(state.search.toLowerCase()))
  }
})

const route = useRoute()
const passcode = route.params.passcode;

const getTeamPasscodes = async () => {
  const pastCodeRequest = await fetch("https://docs.google.com/spreadsheets/d/e/2PACX-1vTYBmQ7Vwo4ttP6MIJXlvowR968cxulaVIG9jSo9174BlEckmEs0nlVAMi1Mlg5L8jvCc7MrR3ScaKa/pub?gid=32278501&single=true&output=csv");
  const pasCode = await pastCodeRequest.text();
  const parsedSheet = Papa.parse(pasCode, {header: true}) as LooseObject;
  const teamName = parsedSheet.data.find((x: {
    [x: string]: string | string[];
  }) => x['Passcode'] === passcode);
  if (teamName) {
    state.teamName = teamName.Team
  }
}

onMounted(async () => {
  const getCheckedTilesRequest =
      await fetch("https://docs.google.com/spreadsheets/d/e/2PACX-1vTYBmQ7Vwo4ttP6MIJXlvowR968cxulaVIG9jSo9174BlEckmEs0nlVAMi1Mlg5L8jvCc7MrR3ScaKa/pub?gid=0&single=true&output=csv")
  const getaCheckedTiles = await getCheckedTilesRequest.text()
  reactiveGSheet.value = Papa.parse(getaCheckedTiles, {header: true}).data as LooseObject[];

  if(passcode){
    await getTeamPasscodes();
  }

  let picIndex = 0;
  reactiveBingo.value = reactiveGSheet.value.map(row => {
    let completed = false;
    let partial = '';
    if(passcode){
      const tileCompletion = row[state.teamName];
      completed = tileCompletion == 1;
      if (!completed && tileCompletion != '') {
        partial = tileCompletion;
      }
    }
    const picName = picIndex.toString();
    picIndex++;
    return {
      tileName: row.Item,
      description: row.Description,
      picName: picName,
      complete: completed,
      portionCompleted: partial,
    } as unknown as BingoTile;
  }) as BingoTile[]
})


const start = new Date("2024-02-16T18:00:00Z")
const end = new Date("2024-02-26T00:00:00Z")
</script>

<template>


  <div class="p-3">

    <div class="text-center mt-10">
      <h1 class="text-3xl">Insomniacs B-I-N-G-O</h1>
      <span class="text-1xl font-bold">{{ start.toLocaleString() }} till {{ end.toLocaleString() }}</span>
    </div>
    <div class="text-center mt-3 mb-2">
      <h1 class="text-3xl" v-show="state.teamName != ''">Team: {{ state.teamName }}</h1>
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

        <div v-if="item.complete" class="cursor-pointer done" v-on:click="openModal(item)">
          <div class="tile-text line-through pt-4">{{ item.tileName }}</div>
        </div>

        <div v-else class="cursor-pointer text-center" v-on:click="openModal(item)">
          <img :src="`./tiles/${item.picName}.png?forcedupdate=1`" class="object-contain max-w-full rounded-lg ">
          <span v-if="item.portionCompleted !== '0'" class="tile-text ">{{ item.portionCompleted }}</span>
        </div>
      </div>


    </div>

    <!-- The Modal -->

    <dialog id="tile details" :class="{'modal  modal-bottom sm:modal-middle': true, 'modal-open': state.modal}">
      <div class="modal-box">
        <h3 class="font-bold text-lg">{{ state.tile.tileName }}</h3>
                      <p class="py-4">{{ state.tile.description }}</p>
        <div class="flex justify-center text-center">
          <img :src="`./tiles/${state.tile.picName}.png?forcedUpdate=1`" alt="bingo tile">

        </div>
        <div v-show="state.tile.portionCompleted" class="text-center">
          <p v-if="state.tile.portionCompleted !== '0'">{{ state.tile.portionCompleted }}</p>
        </div>
        <div class="modal-action">
          <form method="dialog">
            <!-- if there is a button in form, it will close the modal -->
            <button class="btn" @click="() => closeModal()">Close</button>
          </form>
        </div>
      </div>
    </dialog>



  </div>

</template>

<style scoped>

.done {
  width: 101px;
  height: 87.5px;
  background: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' version='1.1' preserveAspectRatio='none' viewBox='0 0 100 100'><path d='M100 0 L0 100 ' stroke='black' stroke-width='1'/><path d='M0 0 L100 100 ' stroke='black' stroke-width='1'/></svg>");
  background-repeat: no-repeat;
  background-position: center center;
}

.bingo-tile {
  cursor: pointer;
}
</style>
