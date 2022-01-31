<script>
    import Button from "../components/Button.svelte";

    export let threads;
    export let thread;

    const defaultThread = {
        general: {
            id: '',
            title: '',
            cover: '',
            url: '',
            slug: '',
        },
        cards: [
            {
                title: '',
                data: {},
            }
        ],
    };

    const selectThread = (t) => () => {
        thread = t || defaultThread;
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