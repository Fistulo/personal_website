<script lang="ts">
  import { Accordion } from "bits-ui";
  import CaretDown from "phosphor-svelte/lib/CaretDown";

  type FaqItem = {
    value: string;
    question: string;
    answer: string;
    isLoading?: boolean;
  };

  let faq_1: FaqItem = {
    value: "faq_1",
    question: "Question 1?",
    answer: "Answer to question 1.",
  };

  let faq_2: FaqItem = {
    value: "faq_2",
    question: "Question 2?",
    answer: "Answer to question 2.",
  };

  let faq_items: FaqItem[] = [faq_1, faq_2];
  let newQuestion = "";
  let isSubmitting = false;

async function addQuestion() {
    if (newQuestion.trim() && !isSubmitting) {
      isSubmitting = true;
      const questionValue = `faq_${Date.now()}`;
      
      // Add item with loading state
      const newItem: FaqItem = {
        value: questionValue,
        question: newQuestion,
        answer: "Loading answer...",
        isLoading: true
      };
      faq_items = [...faq_items, newItem];
      
      const currentQuestion = newQuestion;
      newQuestion = ""; // Clear input immediately

      try {
        // Call backend API
        const response = await fetch('/api/ask', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ question: currentQuestion })
        });

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        
        // Update the answer
        faq_items = faq_items.map(item => 
          item.value === questionValue 
            ? { ...item, answer: data.answer, isLoading: false }
            : item
        );
      } catch (error) {
        console.error('Error fetching answer:', error);
        
        // Update with error message
        faq_items = faq_items.map(item => 
          item.value === questionValue 
            ? { ...item, answer: "Sorry, I couldn't get an answer. Please try again.", isLoading: false }
            : item
        );
      } finally {
        isSubmitting = false;
      }
    }
  }

  function handleKeydown(event: KeyboardEvent) {
    if (event.key === "Enter") {
      addQuestion();
    }
  }
</script>

<div class="flex flex-col items-center w-full px-4 mt-12 md:mt-20">
  <!-- Hero Section -->
  <div class="grid grid-cols-1 md:grid-cols-2 gap-8 w-full max-w-4xl mb-12 items-center">
    <div class="order-2 md:order-1">
      <h1 class="text-4xl md:text-5xl font-bold mb-4">Lennart Lais</h1>
      <p class="text-lg text-gray-600">mini text about me</p>
    </div>
    <img 
      src="piohela_bild.jpg" 
      alt="Portrait Lennart Lais" 
      class="order-1 md:order-2 w-full max-w-sm mx-auto rounded-lg shadow-lg object-cover aspect-square"
    />
  </div>

  <!-- FAQ Section -->
  <Accordion.Root class="w-full max-w-4xl" type="multiple">
    {#each faq_items as item (item.value)}
      <Accordion.Item
        value={item.value}
        class="border-dark-10 group border-b px-1.5"
      >
        <Accordion.Header>
          <Accordion.Trigger
            class="flex w-full flex-1 select-none items-center justify-between py-5 text-[15px] font-medium transition-all [&[data-state=open]>span>svg]:rotate-180"
          >
            <span class="w-full text-left">
              {item.question}
            </span>
            <span
              class="hover:bg-dark-10 inline-flex size-8 items-center justify-center rounded-[7px] bg-transparent"
            >
              <CaretDown class="size-[18px] transition-transform duration-200" />
            </span>
          </Accordion.Trigger>
        </Accordion.Header>
        <Accordion.Content
          class="data-[state=closed]:animate-accordion-up data-[state=open]:animate-accordion-down overflow-hidden text-sm tracking-[-0.01em]"
        >
          <div class="pb-[25px]">
            {item.answer}
          </div>
        </Accordion.Content>
      </Accordion.Item>
    {/each}

    <!-- Add Question Input -->
    <div class="border-dark-10 border-b px-1.5">
      <div class="flex w-full items-center justify-between py-5 gap-3">
        <input
          type="text"
          bind:value={newQuestion}
          on:keydown={handleKeydown}
          placeholder="Ask your own question..."
          class="flex-1 text-[15px] font-medium bg-transparent outline-none placeholder:text-gray-400"
        />
        <button
          on:click={addQuestion}
          disabled={!newQuestion.trim()}
          class="px-4 py-2 bg-blue-600 text-white rounded-lg text-sm font-medium hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors"
        >
          Ask
        </button>
      </div>
    </div>
  </Accordion.Root>
</div>
