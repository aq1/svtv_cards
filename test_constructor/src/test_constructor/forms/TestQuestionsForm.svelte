<script>
    import Button from '../../components/Button.svelte';
    import Card from '../../components/Card.svelte';
    import TestQuestionField from '../fields/TestQuestionField.svelte';
    import {getQuestion} from '../default-test-values';

    export let questions;

    const addQuestion = () => {
        questions = [...questions, getQuestion()];
    };

    const deleteQuestion = (index) => () => {
        questions = [...questions.slice(0, index), ...questions.slice(index + 1, questions.length)];
    }
</script>

<div class="wrapper">
  {#each questions as question, index}
    <Card>
      <div class="header">
        <div class="header__text">
          Вопрос {index + 1} / {questions.length}
        </div>
        <div class="header__button">
          <Button text="-" callback={deleteQuestion(index)} className="danger"/>
        </div>
      </div>
      <TestQuestionField bind:question/>
    </Card>
  {/each}
  <Button text="+ вопрос" callback={addQuestion}/>
</div>

<style>
    .wrapper {
        display: flex;
        flex-direction: column;
        gap: 10px;
    }

    .header {
        display: flex;
        justify-content: space-between;
    }

    .header__text {
        flex: 1 1 70%;
    }

    .header__button {
        width: 36px;
    }
</style>
