<script>
    import Button from "../components/Button.svelte";
    import {thread} from './stores';

    export let threads;

    const selectThread = (t) => () => {
        if (t) {
          thread.set(t);
        } else {
            thread.reset();
        }
    };
</script>

<div>
  {#if threads}
    <Button text="Новый тред" callback={selectThread()}/>
    {#each threads as t}
      <Button text={t.general.title} callback={selectThread(t)}/>
    {/each}
  {/if}
</div>

<style>
    div {
        padding-top: 10px;
        display: flex;
        flex-direction: column;
        gap: 10px;
    }
</style>