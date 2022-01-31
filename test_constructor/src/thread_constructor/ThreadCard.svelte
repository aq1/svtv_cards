<script>
    import EditorJS from '@editorjs/editorjs';
    import List from '@editorjs/list';
    import Embed from '@editorjs/embed';
    import ImageTool from '@editorjs/image';

    import Card from '../components/Card.svelte';
    import Button from "../components/Button.svelte";
    import Input from "../components/Input.svelte";

    import {API_URL} from "./default-thread-values";

    export let card;
    export let index;
    export let removeCard;

    const id = `editor-${index}`;

    const editor = new EditorJS({
        holder: id,
        minHeight: 0,
        data: card.data,
        tools: {
            embed: {
                class: Embed,
                config: {
                    services: {
                        youtube: true,
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
        }
    });
</script>

<Card>
  <div class="wrapper">
    <div class="row">
      <Input type="text" bind:value={card.title} placeholder="Заголовок"/>
      <div class="button">
        <Button text="-" callback={removeCard} className="danger"/>
      </div>
    </div>
    <div {id} class="editor"></div>
  </div>
</Card>


<style>
    .wrapper {

    }

    .row {
        display: flex;
        flex-direction: row;
        gap: 10px;
    }

    .button {
        flex: 40px;
    }

    .editor {
        padding: 10px;
    }
</style>
