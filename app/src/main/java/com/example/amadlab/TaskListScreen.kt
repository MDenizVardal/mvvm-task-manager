package com.example.amadlab

import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.Button
import androidx.compose.material3.Checkbox
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.material3.TopAppBar
import androidx.compose.material3.TopAppBarDefaults
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.style.TextDecoration
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import androidx.lifecycle.viewmodel.compose.viewModel
import com.example.amadlab.ui.theme.AmadLabTheme

// Route: thin and stateful - gets the view model, collects the state, passes the events
@Composable
fun TaskListRoute(
    onTaskClick: (Long) -> Unit,
    onStatisticsClick: () -> Unit,
    viewModel: TasksViewModel = viewModel()
) {
    val state by viewModel.uiState.collectAsStateWithLifecycle()
    TaskListScreen(
        state = state,
        onTitleChange = viewModel::onTitleChange,
        onAdd = viewModel::addTask,
        onToggle = viewModel::toggle,
        onFilterChange = viewModel::onFilterChange,
        onTaskClick = onTaskClick,
        onStatisticsClick = onStatisticsClick
    )
}

// Screen: stateless - draws the UI state and reports the events
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun TaskListScreen(
    state: TasksUiState,
    onTitleChange: (String) -> Unit,
    onAdd: () -> Unit,
    onToggle: (Long) -> Unit,
    onFilterChange: (TaskFilter) -> Unit,
    onTaskClick: (Long) -> Unit,
    onStatisticsClick: () -> Unit
) {
    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Tasks") },
                // Task 3.4: opens the Statistics destination
                actions = { TextButton(onClick = onStatisticsClick) { Text("Statistics") } },
                colors = TopAppBarDefaults.topAppBarColors(
                    containerColor = MaterialTheme.colorScheme.primaryContainer
                )
            )
        }
    ) { innerPadding ->
        Column(
            modifier = Modifier
                .padding(innerPadding)
                .padding(16.dp)
        ) {
            Row(verticalAlignment = Alignment.CenterVertically) {
                OutlinedTextField(
                    value = state.newTitle,
                    onValueChange = onTitleChange,
                    label = { Text("New task") },
                    singleLine = true,
                    modifier = Modifier.weight(1f)
                )
                Spacer(Modifier.width(8.dp))
                Button(onClick = onAdd, enabled = state.canAdd) { Text("Add") }
            }
            // Task 3.2: the buttons only report the chosen filter; the list comes filtered
            Row(
                modifier = Modifier.padding(top = 8.dp),
                horizontalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                TaskFilter.entries.forEach { f ->
                    if (f == state.filter) {
                        Button(onClick = { onFilterChange(f) }) { Text(f.label) }
                    } else {
                        OutlinedButton(onClick = { onFilterChange(f) }) { Text(f.label) }
                    }
                }
            }
            Text(
                "Done: ${state.doneCount} / ${state.totalCount}   (shown: ${state.tasks.size})",
                modifier = Modifier.padding(vertical = 8.dp)
            )
            LazyColumn(modifier = Modifier.fillMaxSize()) {
                items(state.tasks, key = { it.id }) { task ->
                    TaskRow(
                        task = task,
                        onToggle = { onToggle(task.id) },
                        onClick = { onTaskClick(task.id) }
                    )
                    HorizontalDivider()
                }
            }
        }
    }
}

@Composable
fun TaskRow(task: Task, onToggle: () -> Unit, onClick: () -> Unit, modifier: Modifier = Modifier) {
    Row(
        modifier = modifier
            .fillMaxWidth()
            .clickable(onClick = onClick),
        verticalAlignment = Alignment.CenterVertically
    ) {
        Checkbox(checked = task.done, onCheckedChange = { onToggle() })
        Text(
            text = task.title,
            modifier = Modifier.weight(1f),
            textDecoration = if (task.done) TextDecoration.LineThrough else null
        )
        Text(
            text = "details >",
            style = MaterialTheme.typography.labelMedium,
            color = MaterialTheme.colorScheme.primary,
            modifier = Modifier.padding(end = 8.dp)
        )
    }
}

@Preview(showBackground = true)
@Composable
fun TaskListScreenPreview() {
    AmadLabTheme {
        TaskListScreen(
            state = TasksUiState(
                tasks = listOf(Task(1, "Install Android Studio", done = true), Task(2, "Learn Compose")),
                totalCount = 2,
                doneCount = 1
            ),
            onTitleChange = {}, onAdd = {}, onToggle = {}, onFilterChange = {},
            onTaskClick = {}, onStatisticsClick = {}
        )
    }
}
