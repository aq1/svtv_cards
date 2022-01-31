<script>
    import {onMount} from 'svelte';
    import {API_URL} from './default-thread-values';

    import ThreadForm from "./ThreadForm.svelte";
    import SplideControls from "../components/SplideControls.svelte";
    import {Splide, SplideSlide} from "@splidejs/svelte-splide";
    import ThreadSelectForm from "./ThreadSelectForm.svelte";

    let threads;
    let thread;
    let splide;

    const getThreads = () => {
        fetch(`${API_URL}/threads/`).then((response) => {
            response.json().then((json) => {
                threads = [];
                for (let t of json.threads) {
                    threads = [...threads, JSON.parse(t)];
                }
            });
        });
    };
    onMount(getThreads);

    const slides = [
        'Выбрать треды',
        'Редактор',
    ];

    const options = {
        perPage: 1,
        gap: '10px',
        perMove: 1,
        arrows: false,
        pagination: false,
        keyboard: false,
        drag: false,
        wheel: false,
        width: '100%',
        waitForTransition: false,
    };
</script>

{#if threads}
  <SplideControls {slides} {splide}/>
  <Splide {options} bind:this={ splide }>
    <SplideSlide>
      <ThreadSelectForm {threads} bind:thread/>
    </SplideSlide>
    <SplideSlide>
      {#if thread}
        <ThreadForm {thread}/>
      {/if}
    </SplideSlide>
  </Splide>
{/if}

{#if thread}
  <pre>
    {JSON.stringify(thread, null, 4)}
  </pre>
{/if}
<style>

</style>