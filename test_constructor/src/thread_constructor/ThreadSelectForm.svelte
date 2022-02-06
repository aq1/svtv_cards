<script>
    import Button from "../components/Button.svelte";
    import {thread} from './stores';
    import Card from "../components/Card.svelte";

    export let threads;

    const selectThread = (t) => () => {
        if (t) {
          thread.set(t);
        } else {
            thread.reset();
        }
    };
</script>

<Card>
  {#if threads}
    <Button text="Новый тред" callback={selectThread()} className="success"/>
    {#each threads as t}
      <Button text={t.general.title} callback={selectThread(t)}/>
    {/each}
  {/if}
</Card>

<style>
    div {
        padding-top: 10px;
        display: flex;
        flex-direction: column;
        gap: 10px;
    }
</style>