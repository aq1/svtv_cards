<script>
    import {thread} from './stores';
    import ThreadCard from './ThreadCard.svelte';
    import Button from "../components/Button.svelte";
    import Input from "../components/Input.svelte";
    import ImageInput from "../components/ImageInput.svelte";

</script>

<div>
  <div>
    <Input placeholder="Заголовок треда" bind:value={$thread.general.title}/>
    <Input placeholder="URL Slug" bind:value={$thread.general.slug}/>
    <ImageInput name="Обложка" bind:value={$thread.general.cover}/>
  </div>
  {#each $thread.cards as card, index}
    <ThreadCard bind:card {index}/>
  {/each}
</div>

<style>
    div {
        display: flex;
        flex-direction: column;
        gap: 10px;
    }
</style>