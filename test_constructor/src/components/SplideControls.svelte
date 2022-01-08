<script>
    import Button from './Button.svelte';
    import Card from './Card.svelte';

    export let splide;
    export let slides = [];
    let currentIndex = 0;

    const go = (index) => () => {
        currentIndex = index;
        splide.splide.Components.Controller.go(index);
        document.body.scrollIntoView(true);
    };
</script>

<Card>
  {#if splide}
    <div class="splide-controls">
      {#each slides as slide, index}
        <div class="splide-controls__button">
          <Button text={slide} callback={go(index)} className="{currentIndex === index ? 'test' : '' }"/>
        </div>
      {/each}
    </div>
  {/if}
</Card>


<style>
    .splide-controls {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 10px;
    }

</style>