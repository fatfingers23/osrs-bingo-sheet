<script setup lang="ts">
import {computed, onMounted, reactive, ref, watch} from 'vue'
// eslint-disable-next-line no-undef
import Papa from 'papaparse'
import {useRoute} from 'vue-router'
import JSConfetti from 'js-confetti'

const confetti = new JSConfetti();

const jarPics = [
    "https://oldschool.runescape.wiki/images/Jar_of_chemicals_detail.png?c118f",
    "https://oldschool.runescape.wiki/images/Jar_of_darkness_detail.png?c118f",
    "https://oldschool.runescape.wiki/images/Jar_of_decay_detail.png?c118f",
    "https://oldschool.runescape.wiki/images/Jar_of_dirt_detail.png?f533d",
    "https://oldschool.runescape.wiki/images/Jar_of_dreams_detail.png?f533d",
    "https://oldschool.runescape.wiki/images/thumb/Jar_of_eyes_detail.png/180px-Jar_of_eyes_detail.png?f533d",
    "https://oldschool.runescape.wiki/images/Jar_of_miasma_detail.png?f533d",
    "https://oldschool.runescape.wiki/images/Jar_of_sand_detail.png?f533d",
    "https://oldschool.runescape.wiki/images/Jar_of_smoke_detail.png?f533d",
    "https://oldschool.runescape.wiki/images/Jar_of_souls_detail.png?e6cf8",
    "https://oldschool.runescape.wiki/images/Jar_of_spirits_detail.png?e6cf8",
    "https://oldschool.runescape.wiki/images/Jar_of_stone_detail.png?e6cf8",
    "https://oldschool.runescape.wiki/images/Jar_of_swamp_detail.png?e6cf8"
]


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

type EasterEggs = {
  reelBigFish: boolean,
  nice: boolean,
  btw: boolean,
  //new ones
  pause: boolean,
  clown: boolean,
  screenRotation: number,
  zulrahTileRotate: number,
  jar: boolean,
  lastRandomJar: string,
  nerd: boolean,
  youveWon: boolean,
  really: boolean,
  nex: boolean
}

const reactiveBingo = ref([] as BingoTile[]);
const reactiveGSheet = ref([] as LooseObject[]);
let reactiveEasterEggs = ref({
  reelBigFish: false,
  neverGiveUp: false,
  nice:false,
  btw: false,
  pause: false,
  clown: false,
  screenRotation: 0,
  zulrahTileRotate: 0,
  jar: false,
  lastRandomJar: '',
  nerd: false,
  youveWon: false,
  really: false,
  nex: false

} as EasterEggs);

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
  }),
  playing: false,
  pauseWasClicked: false
});


document.addEventListener('keyup', function (evt) {
  if (evt.key === 'Escape') {
    closeModal()
  }
  if(evt.key == "ArrowRight") {
    reactiveEasterEggs.value.screenRotation += 5;
    if (reactiveEasterEggs.value.screenRotation >= 360) {
      reactiveEasterEggs.value.screenRotation = 0;
    }
  }

  if(evt.key == "ArrowLeft") {
    reactiveEasterEggs.value.screenRotation -= 5;
    if (reactiveEasterEggs.value.screenRotation <= 0) {
      reactiveEasterEggs.value.screenRotation = 360;
    }
}

});

function openModal(item: LooseObject): void {
  if(item.picName === '10') {
    reactiveEasterEggs.value.reelBigFish = true;
  }

  if(item.picName === '0') {
    startRotation()
  }

  if(item.picName === '69') {
    reactiveEasterEggs.value.nice = true;
  }

  if(item.picName === '63') {
    reactiveEasterEggs.value.nerd = true;
  }

  if(item.picName === '34') {
    reactiveEasterEggs.value.nex = true;
  }

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

const rickRoll = [
    'never',
    'gonna',
    'going',
    'give',
    'up',
    'roll',
    'rick roll'
]


const filterList = computed(() => {
  //This is needed cause the new bingo sheet goes pass the lines of bingo items
  if (state.search === '') {
    return reactiveBingo.value
  } else {
    if (rickRoll.includes(state.search.toLowerCase())) {
      window.location.href = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ&autoplay=1';
    }
    return reactiveBingo.value.filter(tile => tile.tileName.toLowerCase().includes(state.search.toLowerCase()))
  }
})

watch(state, async () => {
  if(state.search.toLowerCase() === 'btw') {
    reactiveEasterEggs.value.btw = true;
  }else {
    reactiveEasterEggs.value.btw = false;
  }

  if(state.search.toLowerCase() === 'look at you go') {
    await confetti.addConfetti();
  }

  if(state.search.toLowerCase() === '🤡' || state.search.toLowerCase() === 'clown') {
    reactiveEasterEggs.value.clown = true;
  }

  if(state.search.toLowerCase() === 'jar'){
    reactiveEasterEggs.value.jar = true;
    document.body.classList.add('jar-background');
  }

});

const route = useRoute()
const passcode = route.params.passcode;

const getTeamPasscodes = async () => {
  const passCodeRequest = await fetch(import.meta.env.VITE_GSHEET_PASS_CODE_URL);
  const pasCode = await passCodeRequest.text();
  const parsedSheet = Papa.parse(pasCode, {header: true}) as LooseObject;
  const teamName = parsedSheet.data.find((x: {
    [x: string]: string | string[];
  }) => x['Passcode'] === passcode);
  if (teamName) {
    state.teamName = teamName.Team
  }
}

let audioElement: HTMLAudioElement;

const stopMusic = () => {
  //@ts-ignore
  document.querySelector("audio").pause();
  state.playing = false
  state.pauseWasClicked = true;
  audioElement.removeEventListener("pointerup", playMusic);
}

const pleaseGodMakeItStop = () => {
  stopMusic()
  localStorage.setItem('stopMusic', 'true');
}

const playMusic = () => {
  // User interacted with the page. Let's play audio!
  if (!state.pauseWasClicked) {


    audioElement
        .play()
        .then(() => {
          state.playing = true
          console.log("Audio is playing");
        })
        .catch((error) => {
          console.error(error);
        });
  }
};

let intervalTime = 1000; // Start with 1 second interval
const minIntervalTime = 10; // Minimum interval time to speed up to
const decrementStep = 50; // Decrease interval time by 50ms each step

const increaseZulrahTileRotate = () => {
  reactiveEasterEggs.value.zulrahTileRotate += 5; // Increase rotation by 5 degrees
  if (reactiveEasterEggs.value.zulrahTileRotate >= 360) {
    reactiveEasterEggs.value.zulrahTileRotate = 0; // Reset rotation after a full circle
  }
};

const startRotation = () => {
  const rotate = () => {
    increaseZulrahTileRotate();
    if (intervalTime > minIntervalTime) {
      intervalTime -= decrementStep; // Decrease interval time to speed up
    }
    setTimeout(rotate, intervalTime);
  };
  rotate();
};


onMounted(async () => {

  const localStorageStopMusic = localStorage.getItem('stopMusic');

  if (!localStorageStopMusic) {
    //@ts-ignore
    audioElement = document.querySelector("audio");
    let searchBar = document.getElementById("search");
    //@ts-ignore
    searchBar.addEventListener("pointerup", playMusic);
  }

  const getCheckedTilesRequest =
      await fetch(import.meta.env.VITE_GSHEET_BINGO_ITEMS_URL)
  const getaCheckedTiles = await getCheckedTilesRequest.text()
  let temp = Papa.parse(getaCheckedTiles, {header: true}).data as LooseObject[];
  reactiveGSheet.value = temp.slice(0, 65);

  if (passcode) {
    await getTeamPasscodes();
  }

  let picIndex = 0;
  reactiveBingo.value = reactiveGSheet.value.map(row => {
    let completed = false;
    let partial = '';
    if (passcode) {
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

  const didYouWin = Math.random() < 0.10;
  if (didYouWin) {
    reactiveEasterEggs.value.youveWon = true;
    await confetti.addConfetti();
  }

})

const hiddenButton = () => {
  console.log(`
  ⢀⣠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⣠⣤⣶⣶
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⢰⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⣀⣀⣾⣿⣿⣿⣿
⣿⣿⣿⣿⣿⡏⠉⠛⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣿
⣿⣿⣿⣿⣿⣿⠀⠀⠀⠈⠛⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠛⠉⠁⠀⣿
⣿⣿⣿⣿⣿⣿⣧⡀⠀⠀⠀⠀⠙⠿⠿⠿⠻⠿⠿⠟⠿⠛⠉⠀⠀⠀⠀⠀⣸⣿
⣿⣿⣿⣿⣿⣿⣿⣷⣄⠀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⣴⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⡟⠀⠀⢰⣹⡆⠀⠀⠀⠀⠀⠀⣭⣷⠀⠀⠀⠸⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⠃⠀⠀⠈⠉⠀⠀⠤⠄⠀⠀⠀⠉⠁⠀⠀⠀⠀⢿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⢾⣿⣷⠀⠀⠀⠀⡠⠤⢄⠀⠀⠀⠠⣿⣿⣷⠀⢸⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⡀⠉⠀⠀⠀⠀⠀⢄⠀⢀⠀⠀⠀⠀⠉⠉⠁⠀⠀⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣧⠀⠀⠀⠀⠀⠀⠀⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿
  `);
  alert("Check the console!");

}


const start = new Date("2024-08-16T00:00:00Z")
const end = new Date("2024-08-26T00:00:00Z")


const _second = 1000;
const _minute = _second * 60;
const _hour = _minute * 60;
const _day = _hour * 24;
// @ts-ignore
let timer: Timeout;

const countDown = reactive({
  days: 0,
  hours: 0,
  minutes: 0,
  seconds: 0,
  bingoIsGoing: false
});

const showRemaining = () => {
  let now = new Date();
  let endTimeToUse: Date;
  if (now > start) {
    countDown.bingoIsGoing = true;
    endTimeToUse = end;
  } else {
    endTimeToUse = start;
  }
  // @ts-ignore
  let distance = endTimeToUse - now;
  if (distance < 0) {

    clearInterval(timer);
    return;
  }
  countDown.days = Math.floor(distance / _day);
  countDown.hours = Math.floor((distance % _day) / _hour);
  countDown.minutes = Math.floor((distance % _hour) / _minute);
  countDown.seconds = Math.floor((distance % _minute) / _second);

}

timer = setInterval(showRemaining, 1000);

const randomTrueFalse =  Math.random() < 0.5;

</script>

<template>
  <audio>
    <source src="/tiles/scapeMain.mp3" type="audio/mpeg"/>
  </audio>

  <div class="p-3">
    <div :style="{transform: `rotate(${reactiveEasterEggs.screenRotation}deg)`}">
    <small class="super-small">at the bottom right</small>
    <div class="text-center mt-10">
      <h1 class="text-3xl">Back to <span v-if="randomTrueFalse" class="line-through">school</span> <span v-else class="line-through">work</span> Scape bingo</h1>
      <small class="super-small">look at the top left</small>
      <br>
      <span class="text-1xl font-bold">{{ start.toLocaleString() }} till {{ end.toLocaleString() }}</span>
    </div>
    <div class="flex justify-center">
      <div class="flex flex-col">
        <div class="flex justify-center">
          <div class="flex flex-row">
            <div v-show="countDown.days != 0" class="pr-1 text-accent">{{ countDown.days }} days</div>
            <div v-show="countDown.hours != 0" class="pr-1 text-accent">{{ countDown.hours }} hours</div>
            <div v-show="countDown.minutes != 0" class="pr-1 text-accent">{{ countDown.minutes }} minutes</div>
            <div v-show="countDown.seconds != 0" class="pr-1 text-accent">{{ countDown.seconds }} seconds</div>
            <div v-if="countDown.bingoIsGoing">Till bingo ends</div>
            <div v-else>Till bingo starts</div>
          </div>
        </div>
      </div>
    </div>
    <div class="text-center mt-3 mb-2">
      <h1 class="text-3xl" v-show="state.teamName != ''">Team: {{ state.teamName }}</h1>
      <h1 class="text-3xl" v-show="state.totalComplete !== 0">Total Tiles Completed: {{ state.totalComplete }}</h1>
    </div>
    <div class="flex justify-center">
      <div class="form-control">
        <div class="input-group ">
          <input id="search" type="text" placeholder="Search…" class="input input-bordered " v-model="state.search"/>
          <button class="btn btn-square" v-on:click="state.search = ''" >
            X
          </button>
        </div>
      </div>

    </div>
    <div v-if="state.playing" class="flex justify-center pt-3">
      <button class="btn btn-circle  bg-amber-50 w-12 rounded" @click="stopMusic">
        <svg height="48" viewBox="0 0 48 48" width="48" xmlns="http://www.w3.org/2000/svg"><path d="M0 0h48v48H0z" fill="none"/><path d="M18 32h4V16h-4v16zm6-28C12.95 4 4 12.95 4 24s8.95 20 20 20 20-8.95 20-20S35.05 4 24 4zm0 36c-8.82 0-16-7.18-16-16S15.18 8 24 8s16 7.18 16 16-7.18 16-16 16zm2-8h4V16h-4v16z"/></svg>
      </button>
    </div>
    <div v-if="filterList.length == 0 && reactiveBingo.length !== 0" class="flex justify-center pt-2">
      <img v-if="reactiveEasterEggs.btw " :src="`./tiles/btw.png`" class="object-contain max-w-full rounded-lg" alt="btw">
      <img v-else class="object-contain max-w-full rounded-lg " alt="no search results"
           src="https://upload.wikimedia.org/wikipedia/en/8/8d/Super_Mario_Bros_Princess_Is_In_Another_Castle_Quote.png"/>
    </div>

<!--      The bingo sheet-->
    <transition name="fade">

      <div v-if="reactiveBingo.length > 0"
           class="md:p-10 p-5 grid gap-2 md:gap-4 grid-cols-3 grid-rows-2 md:grid-cols-5 md:grid-rows-4">

        <div v-for="(item, index) in filterList" :key="index">
<!--          completed tile-->
          <div v-if="item.complete" class="cursor-pointer done" v-on:click="openModal(item)">
            <div class="line-through pt-4">{{ item.tileName }}</div>
          </div>

<!--          Un completed tile-->
          <div v-else class="flex flex-col cursor-pointer text-center justify-center" v-on:click="openModal(item)">
            <img v-if="reactiveEasterEggs.reelBigFish && item.picName === '10'" :src="`./tiles/reel_big_fish.png`" class="object-contain max-w-full rounded-lg" alt="Reel big fish easter egg">
            <img v-else-if="reactiveEasterEggs.nice && item.picName === '69'" :src="`./tiles/nice.png`" class="object-contain max-w-full rounded-lg" alt="tile 69 nice">
            <img v-else-if="reactiveEasterEggs.clown" :src="`./tiles/dangler_head.png`" class="object-contain max-w-full rounded-lg" alt="clown">
            <img v-else-if="reactiveEasterEggs.nerd && item.picName == '63'" src="https://preview.redd.it/q6qj6v4sqpdc1.jpeg?width=1024&auto=webp&s=4690f1f1b6e58a653f7b5acac8d0cc798c0b0b26" class="object-contain max-w-full rounded-lg" alt="nerd">
            <video v-else-if="reactiveEasterEggs.nex && item.picName === '34'" autoplay loop>
              <source src="https://images-ext-1.discordapp.net/external/Zu1akmHHtjOR9DtAJVrOMIKzmY-Lf4rnjqCa0qxaHtM/https/media.tenor.com/id1cX15kQawAAAPo/nex-osrs.mp4" type="video/mp4">
            </video>
            <img :style="[item.picName == '0' ? {transform: `rotate(${reactiveEasterEggs.zulrahTileRotate}deg)`}: '']" v-else :src="`./tiles/${item.picName}.png?AGAIN`" class="object-contain max-w-full rounded-lg" :alt="`bingo tile for ${item.tileName}`">
            <span class="text-accent ">{{ item.tileName }}</span>
<!--            <span class="text-accent ">{{ item.picName }}</span>-->
            <span v-if="item.portionCompleted !== '0'" class="text-secondary">{{ item.portionCompleted }}</span>
          </div>
          <div class="flex justify-center">
          <small v-if="item.picName === '15'" class="super-small">Go to the search bar and enter the first word of each message in order!</small>
          </div>
        </div>
        <template v-if="reactiveEasterEggs.jar" >
          <img v-for="(jar, index) in jarPics" :key="index" :src="jar" class="object-contain max-w-full rounded-lg" alt="jar">
        </template>
      </div>
      <div v-else class="text-center mt-10">
        <span>Loading the mother of all bingo sheets</span>
        <br>
        <span class="loading loading-spinner loading-lg"></span>
      </div>
    </transition>


    <div class="flex justify-center p-6 md:p-10">
      <a @click="pleaseGodMakeItStop" class="text-sm underline cursor-pointer">
        if the audio is playing and annoying you can click here to permanently stop it
      </a>
    </div>
    <div class="flex justify-end">
      <small class="super-small">You need to check under the "Broken Pickaxe"</small>
    </div>
    <button class="hidden btn btn-outline" @click="hiddenButton">What happens if you click me?</button>
    </div>

    <!-- The Modal -->

    <dialog id="tile details" :class="{'modal sm:modal-middle': true, 'modal-open': state.modal}">
      <div class="modal-box">
        <h3 class="font-bold text-lg">{{ state.tile.tileName }}</h3>
        <p class="py-4">{{ state.tile.description }}</p>
        <div class="flex justify-center text-center">
          <img :src="`./tiles/${state.tile.picName}.png?AGAIN`" alt="bingo tile">

        </div>
        <div v-show="state.tile.portionCompleted" class="text-center">
          <p v-if="state.tile.portionCompleted !== '0'">{{ state.tile.portionCompleted }}</p>
        </div>
        <div class="modal-action">
          <form method="dialog">
            <button class="btn" @click="() => closeModal()">Close</button>
          </form>
        </div>
      </div>
    </dialog>


    <dialog id="youve-won" :class="{'modal sm:modal-middle': true, 'modal-open': reactiveEasterEggs.youveWon}">
      <div class="modal-box text-center">
        <h3 class="font-bold text-lg uppercase">🎉 YOU HAVE WON AN IPAD 🎉</h3>
        <div class="flex flex-col justify-center pt-5">

          <img v-if="reactiveEasterEggs.really" src="https://media1.tenor.com/m/7mbgg5rcJ1wAAAAd/justin-timberlake.gif" alt="really">
          <button class="btn btn-primary" @click="() => reactiveEasterEggs.really = true">Claim your 🎁 </button>
        </div>
        <div class="modal-action">
          <form method="dialog">
            <button class="btn" @click="() => reactiveEasterEggs.youveWon = false">Close</button>
          </form>
        </div>
      </div>
    </dialog>


  </div>

</template>

<style >

.super-small {
  font-size: 2px;
}

.done {
  width: 101px;
  height: 88px;
  background: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' version='1.1' preserveAspectRatio='none' viewBox='0 0 100 100'><path d='M100 0 L0 100 ' stroke='black' stroke-width='1'/><path d='M0 0 L100 100 ' stroke='black' stroke-width='1'/></svg>") no-repeat center center;
}

.jar-background {
  background-image:  url("https://oldschool.runescape.wiki/images/Jar_of_darkness_detail.png?c118f");
  background-repeat: space;

  background-size: 100px;
}

</style>
