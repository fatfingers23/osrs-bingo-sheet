<script setup lang="ts" xmlns:x-transition="http://www.w3.org/1999/xhtml">
import {reactive, computed} from 'vue'
import bingoSheet from '../bingoSheet.json'
// eslint-disable-next-line no-undef
// import Papa from 'papaparse'
// import { useRoute } from 'vue-router'
interface LooseObject {
    [key: string]: any
}

const reactiveBingo = reactive(bingoSheet);


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

function openModal(item: LooseObject, picIndex: string | number): void {
    state.modal = true;
    state.tile.tileName = item.tileName;
    state.tile.description = item.description;
    state.tile.picName = picIndex.toString()
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


    <div class="container p-3">

        <div class="text-center mt-10">
            <h1 class="text-3xl">B-I-N-G-O</h1>
            <span>00:00 Friday 16th of June (8pm EST Thurday) end Monday 26th of June 00:00 (Sunday 8pm EST)</span>
        </div>
        <!--  <h2>Team: {{teamName}}</h2>-->
        <div class="text-center mt-3">
            <h3 class="text-2xl">Extra Info</h3>
        </div>
        <div class="p-6 md:p-10">
            <p class="">
              Becky will post daily updates in your channels of how your team is doing and possibly updates of the whole spreadsheet after a couple of days if everybody is interested.

              Make sure you read all the information Becky posted from adding you in the channel and follow the screenshots to tick untradeable's on/lowered chat announcement so nothing can be missed.

              Becky will lower the clan announcements down to 100k cover all barrows drops and can increase as the event goes on once all the easier drops are claimed.

              Besides that good luck, have fun, read all the above information and get ready to grind:)

            </p>

            <p>

            </p>
        </div>
        <div class="flex justify-center">
            <div class="form-control">
                <div class="input-group">
                    <input type="text" placeholder="Search…" class="input input-bordered" v-model="state.search"/>
                    <button class="btn btn-square" v-on:click="state.search = ''">
                        X
                    </button>
                </div>
            </div>
        </div>
        <div class="md:p-10 p-5 grid gap-2 md:gap-4 grid-cols-4 grid-rows-2 md:grid-cols-8 md:grid-rows-4">
            <div v-for="(item, index) in filterList" :key="index">
                <div v-if="item.complete" class="bingo-tile done">
                    <!--        <img :src="`./tiles/${item.picName}.png`">-->

                    <div class="tile-text">{{ item.tileName }}</div>
                </div>

                <div v-else class="bingo-tile" v-on:click="openModal(item, index)">
                    <img :src="`./tiles/${index}.png`">
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
                            <div class="flex justify-center">
                            <img :src="`./tiles/${state.tile.picName}.png`" alt="bingo tile">
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
    background: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' version='1.1' preserveAspectRatio='none' viewBox='0 0 100 100'><path d='M100 0 L0 100 ' stroke='black' stroke-width='1'/><path d='M0 0 L100 100 ' stroke='black' stroke-width='1'/></svg>");
    background-repeat: no-repeat;
    background-position: center center;
    background-size: 100% 100%, auto;
    z-index: 1000000;
    color: red;

}
</style>
