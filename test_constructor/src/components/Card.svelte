<div class="card">
  <slot></slot>
</div>


<style>
    .card {
        background-color: var(--text-primary);
        padding: 15px;
        border: 1px solid rgba(0, 0, 0, .1);
        border-radius: 15px;
        display: flex;
        flex-direction: column;
        gap: 15px;
    }
</style>