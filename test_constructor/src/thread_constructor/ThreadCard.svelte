<script>
    import {thread} from './stores';
    import EditorJS from '@editorjs/editorjs';
    import List from '@editorjs/list';
    import Embed from '@editorjs/embed';
    import ImageTool from '@editorjs/image';

    import Card from '../components/Card.svelte';
    import Button from "../components/Button.svelte";
    import Input from "../components/Input.svelte";

    import {API_URL} from "./default-thread-values";
    import {onDestroy} from 'svelte';
    import EditorContent from "./EditorContent.svelte";

    export let card;
    export let index;

    const id = `editor-${index}`;
    let editor = null;

    onDestroy(() => {
        if (editor) {
            editor.destroy();
        }
    });

    const setEditor = () => {
        if ((card.isActive && editor) || (!card.isActive && !editor)) {
            return;
        }

        if (!card.isActive && editor) {
            editor.destroy();
            editor = null;
            return;
        }

        editor = new EditorJS({
            holder: id,
            minHeight: 0,
            data: card.data,
            placeholder: 'Щелкните чтобы добавить блоки',
            tools: {
                embed: {
                    class: Embed,
                    config: {
                        services: {
                            youtube: true,
                            bitchute: {
                                regex: /https:\/\/www.bitchute.com\/video\/(.*?)\//,
                                embedUrl: 'https://www.bitchute.com/embed/<%= remote_id %>/',
                                html: `<iframe width="640" height="360" scrolling="no" frameborder="0" style="border: none;"></iframe>`,
                            }
                        }
                    }
                },
                list: {
                    class: List,
                    inlineToolbar: true,
                },
                image: {
                    class: ImageTool,
                    config: {
                        endpoints: {
                            byFile: `${API_URL}/upload-file/`,
                        }
                    }
                }
            },
            onChange: (api) => {
                api.saver.save().then((data) => {
                    card.data = data;
                });
            },
            onReady() {
                document.getElementById(id).scrollIntoView({behavior: 'smooth', block: 'center'});
            }
        });
    };


    $: {
        console.log(card.isActive, editor);
        setEditor();
    }

</script>

<Card>
  <div class="wrapper">
    <div class="row">
      <Input type="text" bind:value={card.title} placeholder="Заголовок"/>
      <div class="button">
        <Button text="^" callback={() => thread.moveCard(index, -1)} disabled={index === 0}
                tooltip="Переместить вверх"/>

      </div>
      <div class="button">
        <Button text="˅" callback={() => thread.moveCard(index, 1)} disabled={index === $thread.cards.length - 1} tooltip="Переместить вниз"/>
      </div>
      <div class="button">
        <Button text="-" callback={() => thread.removeCard(index)} className="danger" tooltip="Удалить"/>
      </div>
    </div>
    {#if card.isActive}
      <div {id} class="editor"></div>
    {:else if !card.data.blocks}
      <div class="placeholder" on:click={() => thread.setActiveCard(index)}>
        Нажмите чтобы редактировать
      </div>
    {:else}
      <div on:click={() => thread.setActiveCard(index)}>
        <EditorContent data={card.data}/>
      </div>
    {/if}
  </div>
</Card>


<style>
    .placeholder {
        width: 100%;
        padding: 10px 0;
        text-align: center;
        opacity: .6;
        cursor: pointer;
    }

    .row {
        display: flex;
        flex-direction: row;
        gap: 10px;
    }

    .button {
        flex: 40px 0 0;
    }

    .editor {
        padding: 10px;
    }
</style>
