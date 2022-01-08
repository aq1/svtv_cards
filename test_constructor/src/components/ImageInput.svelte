<script>
    import Input from './Input.svelte';

    export let name = '';
    export let value;
</script>

<div class="wrapper">
  {#if value}
    <div class="image-wrapper">
      <img src="{value}" alt="обложка">
    </div>
  {/if}
  <Input type="image" {name} bind:value/>
</div>


<style>
    .wrapper {
        display: flex;
        flex-direction: column;
        gap: 10px;
    }

    .image-wrapper {
        width: 100%;
        height: 200px;
    }

    img {
        object-fit: cover;
        height: 200px;
        width: 100%;
    }
</style>