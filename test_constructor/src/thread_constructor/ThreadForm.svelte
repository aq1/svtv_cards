<script>
    import {API_URL} from "../test_constructor/default-test-values";
    import ThreadCard from './ThreadCard.svelte';
    import Button from "../components/Button.svelte";
    import Input from "../components/Input.svelte";
    import ImageInput from "../components/ImageInput.svelte";

    export let thread;

    const addCard = () => {
        thread.cards = [...thread.cards, {
            title: '',
            data: {},
        }];
    }

    window.editors = [];

    const removeCard = (index) => () => {
        const cards = thread.cards;
        cards.splice(index, 1);
        thread.cards = cards;
        window.editors.splice(index, 1);
    };

    const save = async () => {
        const response = await fetch(`${API_URL}/save-thread/`, {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(thread),
        });
        if (response.status !== 201) {
            alert('ошибка загрузки');
            const json = await response.json();
            console.log(json);
            return;
        }
        response.json().then((json) => {
            thread.general.id = json.id;
            thread.general.url = json.url;
        });
        alert('Сохранено');
    };
</script>

<div>
  <div>
    <Input placeholder="Заголовок треда" bind:value={thread.general.title}/>
    <Input placeholder="URL Slug" bind:value={thread.general.slug}/>
    <ImageInput name="Обложка" bind:value={thread.general.cover}/>
  </div>
  <div>
    <p>
      <a href="{thread.general.url}" target="_blank">{thread.general.url}</a>
    </p>
  </div>
  {#each thread.cards as card, index}
    <ThreadCard bind:card {index} removeCard={removeCard(index)}/>
  {/each}
  <Button text="+ карточка" callback={addCard}/>
  <Button text="Сохранить" className="success" callback={save}/>
</div>

<style>
    div {
        display: flex;
        flex-direction: column;
        gap: 10px;
    }

    pre {
        overflow: hidden;
    }
</style>