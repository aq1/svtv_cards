<script>
    import {thread} from './stores';
    import {API_URL} from "../test_constructor/default-test-values";
    import Button from "../components/Button.svelte";

    let adminUrl;
    $: if ($thread.general?.url) {
        const origin = (new URL($thread.general.url)).origin;
        adminUrl = `${origin}/ghost/#/editor/post/${$thread.general.id}`;
    }

    const save = async () => {
        const response = await fetch(`${API_URL}/save-thread/`, {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
            },
            body: JSON.stringify($thread),
        });
        if (response.status !== 201) {
            alert('ошибка загрузки');
            const json = await response.json();
            console.log(json);
            return;
        }
        response.json().then((json) => {
            thread.update((thread) => {
                for (let key in json) {
                    thread.general[key] = json[key];
                }
                return thread;
            });
        });
        alert('Сохранено');
    };
</script>

<div>
  <div>
    <p>
      Тред "{$thread.general.title}" / Карточек: <b>{$thread.cards.length}</b> / URL: {$thread.general.slug}
    </p>
  </div>
  <div class="center">
    <img src="{$thread.general.cover}" alt="">
  </div>
  <div class="center">
    <p>
      {#if $thread.general.url}
        <a href="{$thread.general.url}" target="_blank">Превью</a> /
        <a href="{adminUrl}" target="_blank">Админка</a>
      {/if}
    </p>
  </div>
  <Button text="Сохранить" className="success" callback={save}/>
</div>

<style>
    div {
        display: flex;
        flex-direction: column;
        gap: 10px;
    }

    img {
        max-width: 100%;
        max-height: 400px;
    }

    .center {
        display: flex;
        justify-content: center;
    }
</style>