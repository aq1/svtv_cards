<script>
    import Input from '../../components/Input.svelte';
    import ImageInput from '../../components/ImageInput.svelte';
    import Button from '../../components/Button.svelte';

    import {getAnswer} from '../default-test-values';

    export let question;

    const addAnswer = () => {
        question.answers = [...question.answers, getAnswer()];
    };

    const deleteAnswer = (index) => () => {
        question.answers = [...question.answers.slice(0, index), ...question.answers.slice(index + 1, question.answers.length)];
    };
</script>

<div class="wrapper">
  <ImageInput bind:value={question.image}/>
  <Input bind:value={question.text} placeholder="Текст"/>
  <div class="answers">
    <div>Ответы</div>
    {#each question.answers as answer, index}
      <div class="answer">
        <div class="answer__text">
          <Input bind:value={answer.text}/>
        </div>
        <div class="answer__value">
          <Input bind:value={answer.value}/>
        </div>
        <!--      <div class="answer__value">-->
        <!--        <Input bind:value={answer.value} placeholder="Значение"/>-->
        <!--      </div>-->
        <div class="answer__button">
          <Button text="-" callback={deleteAnswer(index)} className="danger"/>
        </div>
      </div>
    {/each}
  </div>
  <div>
    <Input bind:value={question.correct} placeholder="Текст правильного ответа"/>
    <Input bind:value={question.wrong} placeholder="Текст непрвильного ответа"/>
  </div>
  <Button text="+ ответ" callback={addAnswer}/>
</div>


<style>
    .wrapper {
        display: flex;
        flex-direction: column;
        gap: 10px;
    }

    .answers {
        display: flex;
        flex-direction: column;
        gap: 5px;
    }

    .answer {
        display: flex;
        gap: 5px;
    }

    .answer__text {
        flex: 1 1 80%;
    }

    .answer__value {
        flex: 1 0 10%;
    }

    .answer__button {
        width: 38px;
    }
</style>